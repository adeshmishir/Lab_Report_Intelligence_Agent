import re

from app.core.errors import ParserError
from app.core.config import Settings
from app.schemas.extraction import ExtractionOutput, ParserResult, ReferenceRange
from app.services.ingestion.llm_client import LLMClient
from app.services.ingestion.prompts import EXTRACTION_SYSTEM_PROMPT, build_user_prompt
from app.services.ingestion.dates import parse_date
from app.services.ingestion.reference_ranges import parse_reference_range

SPECIAL_MARKERS = re.compile(r"[\[\(]\s*(HIGH|H|LOW|L|OUT OF RANGE|ABNORMAL|CRITICAL)\s*[\]\)]", re.IGNORECASE)


def _extract_range(text: str) -> tuple[float, float, str] | None:
    match = re.search(r"\(?(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)\)?", text)
    if match:
        return float(match.group(1)), float(match.group(2)), match.group(0)
    match = re.search(r"<\s*(\d+(?:\.\d+)?)", text)
    if match:
        return None, float(match.group(1)), match.group(0)
    match = re.search(r">\s*(\d+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1)), None, match.group(0)
    return None


class DeterministicParser:
    """Rule-based parser used when no LLM is configured or for reliability.

    It only extracts values that appear explicitly in the text. Missing fields
    are left as None. It never consults medical knowledge.
    """

    def __init__(self):
        pass

    @staticmethod
    def _find_date(lines: list[str]) -> str | None:
        preferred = {}
        any_candidates = []

        for line in lines:
            low = line.lower()
            dates = re.findall(
                r"(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})",
                line,
                flags=re.IGNORECASE,
            )
            if not dates:
                continue
            if "report date" in low or ("date:" in low and "report" in low):
                preferred.setdefault("report", parse_date(dates[0]))
            elif "collection date" in low or "collection" in low or "collected" in low:
                preferred.setdefault("collection", parse_date(dates[0]))
            elif "generated" in low or "print date" in low:
                preferred.setdefault("generated", parse_date(dates[0]))

        for key in ("report", "collection", "generated"):
            if preferred.get(key):
                return preferred[key].isoformat()
        return None

    @staticmethod
    def _parse_lab_line(line: str) -> ParserResult | None:
        line = SPECIAL_MARKERS.sub("", line).strip()
        if not line:
            return None

        tokens = line.split()

        # Skip pure column header rows.
        first = tokens[0].lower().rstrip(":")
        if first in ("test", "result", "parameter") and "reference" in line.lower():
            return None

        value_idx = None
        qualitative_value = None
        for i, token in enumerate(tokens):
            if re.fullmatch(r"[-+]?\d+(?:[.,]\d+)?", token):
                value_idx = i
                break

        ambiguous = False
        if value_idx is None:
            for i, token in enumerate(tokens):
                if re.fullmatch(r"[-+]?\d*(?:[.,]\d+)?\?+", token) or re.fullmatch(r"xx+", token, re.IGNORECASE):
                    value_idx = i
                    ambiguous = True
                    break

        if value_idx is None:
            qualitative = re.compile(r"positive|negative|trace|detected|not\s+detected", re.IGNORECASE)
            for i, token in enumerate(tokens):
                if qualitative.fullmatch(token) or (
                    token.lower() == "not" and i + 1 < len(tokens) and tokens[i + 1].lower() == "detected"
                ):
                    value_idx = i
                    qualitative_value = "not detected" if token.lower() == "not" else token
                    break

        if value_idx is None:
            return None

        name = " ".join(tokens[:value_idx]).strip(" :\t-|")
        if not name or not re.search(r"[A-Za-z]", name) or len(tokens[:value_idx]) > 6:
            return None

        # Skip date/header-only lines, they are not lab results.
        if any(keyword in name.lower() for keyword in ("date", "collected", "generated", "reported")):
            return None

        raw_value = qualitative_value or tokens[value_idx]
        parsed_value = None
        if re.fullmatch(r"[-+]?\d+(?:[.,]\d+)?", raw_value):
            parsed_value = float(raw_value.replace(",", "."))

        rest = " ".join(tokens[value_idx + (2 if qualitative_value == "not detected" else 1):])
        range_info = _extract_range(rest)
        ambiguous = ambiguous or "?" in rest or "***" in rest or "xx" in rest.lower()

        unit = None
        if rest:
            candidate = re.split(r"\s+", rest)[0]
            range_like = bool(re.search(r"[-–—]", candidate) and re.search(r"\d", candidate))
            range_like = range_like or candidate.startswith(("<", ">")) or bool(re.match(r"\(?\d", candidate))
            if not range_like and not re.fullmatch(r"[-+]?\d+(?:[.,]\d+)?", candidate):
                if not candidate.lower().startswith(("low", "high", "ref", "normal")):
                    unit = candidate

        ref = parse_reference_range(range_info[2]) if range_info else None

        return ParserResult(
            test_name_original=name,
            value_numeric=parsed_value,
            value_text=None if parsed_value is not None else raw_value,
            unit=unit,
            reference_range=ref,
            raw_text=line,
            confidence="low" if ambiguous else "medium",
            data_quality="ambiguous_value" if ambiguous else ("good" if parsed_value is not None else "unreadable"),
        )

    def parse(self, raw_text: str) -> ExtractionOutput:
        lines = [l.strip() for l in raw_text.splitlines()]
        results = []
        for line in lines:
            if not line:
                continue
            parsed = self._parse_lab_line(line)
            if parsed:
                results.append(parsed)

        return ExtractionOutput(report_date=self._find_date(lines), tests=results)


class LLMParser:
    def __init__(self, settings: Settings):
        self.client = LLMClient(settings)

    def parse(self, raw_text: str) -> ExtractionOutput:
        payload = self.client.complete_json(
            EXTRACTION_SYSTEM_PROMPT,
            build_user_prompt(raw_text),
        )
        try:
            return ExtractionOutput.model_validate(payload)
        except Exception as exc:
            raise ParserError() from exc


def build_parser(settings: Settings) -> object:
    mode = settings.EXTRACTION_MODE
    if mode == "llm":
        return LLMParser(settings)
    if mode == "deterministic":
        return DeterministicParser()
    # auto: use the LLM when a key is configured, otherwise the deterministic parser.
    if settings.LLM_API_KEY:
        return LLMParser(settings)
    return DeterministicParser()


def parse_raw_text(raw_text: str, settings: Settings) -> ExtractionOutput:
    parser = build_parser(settings)
    return parser.parse(raw_text)