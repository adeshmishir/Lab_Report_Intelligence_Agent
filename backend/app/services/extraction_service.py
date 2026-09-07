from dataclasses import dataclass
from datetime import date
import hashlib
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import ExtractionEmptyError
from app.core.errors import ProcessingFailedError, DuplicateReportError
from app.models.report import Report, LabResult, ReportStatus
from app.schemas.extraction import ExtractionOutput
from app.services.ingestion.file_validator import validate_file
from app.services.ingestion.text_extractor import TextExtractor
from app.services.ingestion.lab_parser import parse_raw_text
from app.services.ingestion.validators import finalize_results, parse_report_date


@dataclass
class ProcessedReport:
    report_id: int
    report_date: Optional[date]
    tests_extracted: int
    raw_text: str


class ExtractionService:
    def __init__(self, settings: Settings, db: Session):
        self.settings = settings
        self.db = db
        self.text_extractor = TextExtractor(ocr_backend=settings.OCR_BACKEND)

    def process_upload(self, filename: str, content_type: str, data: bytes) -> ProcessedReport:
        # 1. Validate the file (size, type, emptiness).
        file = validate_file(
            filename=filename,
            content_type=content_type,
            data=data,
            max_size=self.settings.MAX_UPLOAD_SIZE,
        )
        content_hash = hashlib.sha256(data).hexdigest()
        existing = self.db.query(Report.id).filter(
            Report.user_id == 1,
            Report.content_hash == content_hash,
        ).first()
        if existing:
            raise DuplicateReportError()

        # 2. Extract raw text from the PDF or image.
        document = self.text_extractor.extract_document(file)
        raw_text = document.raw_text.strip()
        if not raw_text:
            raise ExtractionEmptyError()

        # 3. Parse the raw text into structured candidate fields.
        extraction: ExtractionOutput = parse_raw_text(raw_text, self.settings)

        # 4. Validate + normalize + quality-tag the structured data.
        results = finalize_results(extraction.tests)
        report_date = parse_report_date(extraction.report_date)

        # 5. Persist the report and its results.
        report = Report(
            user_id=1,
            original_filename=file.filename,
            mime_type=file.mime_type,
            content_hash=content_hash,
            report_date=report_date,
            raw_text=raw_text,
            status=ReportStatus.PROCESSED,
        )
        for result in results:
            report.results.append(
                LabResult(
                    test_name_original=result.test_name_original,
                    test_name_normalized=result.test_name_normalized,
                    value_numeric=result.value_numeric,
                    value_text=result.value_text,
                    value_numeric_original=result.value_numeric,
                    value_text_original=result.value_text,
                    unit=result.unit,
                    reference_low=result.reference_range.low if result.reference_range else None,
                    reference_high=result.reference_range.high if result.reference_range else None,
                    reference_text=result.reference_range.text if result.reference_range else None,
                    raw_text=result.raw_text or "",
                    confidence=result.confidence or "medium",
                    data_quality=result.data_quality or "good",
                    critical=result.critical,
                )
            )

        self.db.add(report)
        try:
            self.db.commit()
        except Exception as exc:
            self.db.rollback()
            raise ProcessingFailedError() from exc
        self.db.refresh(report)

        return ProcessedReport(
            report_id=report.id,
            report_date=report_date,
            tests_extracted=len(results),
            raw_text=raw_text,
        )