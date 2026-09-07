from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class ReferenceRange(BaseModel):
    low: Optional[float] = None
    high: Optional[float] = None
    text: Optional[str] = None


class ParserResult(BaseModel):
    test_name_original: str = Field(min_length=1)
    test_name_normalized: Optional[str] = None
    value_numeric: Optional[float] = None
    value_text: Optional[str] = None
    unit: Optional[str] = None
    reference_range: Optional[ReferenceRange] = None
    raw_text: str = Field(default="")
    confidence: str = Field(default="medium")
    data_quality: str = Field(default="good")
    critical: bool = False


class ExtractionOutput(BaseModel):
    patient_name: Optional[str] = None
    report_date: Optional[str] = None
    tests: list[ParserResult] = Field(default_factory=list)


class ExtractedDocument(BaseModel):
    """Internal representation of the text extracted from a source file."""
    source_type: str
    raw_text: str
    extraction_method: str = "unknown"
    pages: list[dict] | None = None