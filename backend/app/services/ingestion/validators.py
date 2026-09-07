from typing import Optional
from collections import defaultdict

from app.schemas.extraction import ParserResult, ReferenceRange
from app.services.ingestion.normalization import normalize_test_name, normalize_unit
from datetime import date

from app.services.ingestion.dates import parse_date


def _has_reference_range(ref: Optional[ReferenceRange]) -> bool:
    return bool(ref and (ref.low is not None or ref.high is not None))


def _assign_quality(result: ParserResult) -> None:
    """Deterministically derive data_quality and confidence from available fields."""
    if result.data_quality == "ambiguous_value":
        result.confidence = "low"
        return
    if result.value_numeric is None and not (result.value_text or "").strip():
        if result.data_quality != "ambiguous_value":
            result.data_quality = "missing_value"
        result.confidence = "low"
    elif not (result.unit or "").strip():
        result.data_quality = "missing_unit"
        result.confidence = "medium"
    elif not _has_reference_range(result.reference_range):
        result.data_quality = "missing_reference_range"
        result.confidence = "medium"
    else:
        result.data_quality = "good"
        result.confidence = "high"


def _flag_duplicates(results: list[ParserResult]) -> None:
    """Flag repeated test names as duplicate or conflicting, preserving every row."""
    groups: dict[str, list[ParserResult]] = defaultdict(list)
    for r in results:
        groups[r.test_name_normalized.casefold()].append(r)

    for group in groups.values():
        if len(group) < 2:
            continue
        signature = [
            (r.value_numeric, r.value_text, (r.unit or "").strip(), r.reference_range.model_dump() if r.reference_range else None)
            for r in group
        ]
        quality = "duplicate_test" if len(set(map(str, signature))) == 1 else "conflicting_values"
        for duplicate in group:
            duplicate.data_quality = quality
            duplicate.confidence = "medium" if quality == "duplicate_test" else "low"


def finalize_results(results: list[ParserResult]) -> list[ParserResult]:
    """Validate, normalize, and quality-tag extracted candidate results."""
    cleaned: list[ParserResult] = []
    seen: set[str] = set()

    for result in results:
        original = (result.test_name_original or "").strip()
        if not original:
            continue
        seen.add(original.casefold())

        result.test_name_original = original
        result.test_name_normalized = normalize_test_name(original)
        result.unit = normalize_unit(result.unit)
        _assign_quality(result)
        cleaned.append(result)

    _flag_duplicates(cleaned)
    return cleaned


def parse_report_date(raw_value: Optional[str]) -> Optional[date]:
    return parse_date(raw_value)