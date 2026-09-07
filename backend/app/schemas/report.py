from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class LabResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    report_id: int
    test_name_original: str
    test_name_normalized: str
    value_numeric: Optional[float] = None
    value_text: Optional[str] = None
    value_numeric_original: Optional[float] = None
    value_text_original: Optional[str] = None
    unit: Optional[str] = None
    reference_low: Optional[float] = None
    reference_high: Optional[float] = None
    reference_text: Optional[str] = None
    raw_text: str
    confidence: str
    data_quality: str
    critical: bool = False
    correction_note: Optional[str] = None
    corrected_at: Optional[datetime] = None


class ReportSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    mime_type: str
    report_date: Optional[date] = None
    status: str
    tests_count: int = 0
    attention_count: int = 0
    created_at: datetime


class ReportDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    mime_type: str
    report_date: Optional[date] = None
    status: str
    created_at: datetime
    raw_text: str
    result_count: int = 0
    results: list[LabResultOut] = []


class UploadResponse(BaseModel):
    report_id: int
    status: str
    report_date: Optional[date] = None
    tests_extracted: int = 0


class CorrectionRequest(BaseModel):
    value_numeric: Optional[float] = None
    value_text: Optional[str] = None
    reason: str = "User correction"