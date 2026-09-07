import re

from app.schemas.extraction import ReferenceRange


def parse_reference_range(text: str | None) -> ReferenceRange | None:
    if not text or not text.strip():
        return None
    original = text.strip()
    number = r"[-+]?\d+(?:[.,]\d+)?"
    match = re.search(rf"({number})\s*(?:-|–|—|to)\s*({number})", original, re.I)
    if match:
        return ReferenceRange(
            low=float(match.group(1).replace(",", ".")),
            high=float(match.group(2).replace(",", ".")),
            text=original,
        )
    match = re.search(rf"<\s*({number})", original)
    if match:
        return ReferenceRange(high=float(match.group(1).replace(",", ".")), text=original)
    match = re.search(rf">\s*({number})", original)
    if match:
        return ReferenceRange(low=float(match.group(1).replace(",", ".")), text=original)
    return ReferenceRange(text=original)