from datetime import date
import re

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

ISO_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
NUMERIC_RE = re.compile(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$")
TEXT_DMY_RE = re.compile(r"^(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\s+(\d{4})$")
TEXT_MDY_RE = re.compile(r"^([A-Za-z]{3,9})\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})$")


def _safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def parse_date(value: str | None) -> date | None:
    """Parse a date string into a ``date``, or None when not confidently determinable."""
    if not value:
        return None

    text = value.strip()

    match = ISO_RE.match(text)
    if match:
        return _safe_date(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    match = TEXT_DMY_RE.match(text)
    if match:
        month = MONTHS.get(match.group(2).lower()[:3])
        return _safe_date(int(match.group(3)), month, int(match.group(1))) if month else None

    match = TEXT_MDY_RE.match(text)
    if match:
        month = MONTHS.get(match.group(1).lower()[:3])
        return _safe_date(int(match.group(3)), month, int(match.group(2))) if month else None

    match = NUMERIC_RE.match(text)
    if match:
        a, b, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if year < 100:
            year += 2000
        # Only parse when unambiguous; otherwise report_date stays null.
        if a > 12:  # day-first
            return _safe_date(year, b, a)
        if b > 12:  # month-first
            return _safe_date(year, a, b)
        return None  # ambiguous MM/DD vs DD/MM

    return None