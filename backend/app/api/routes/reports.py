from fastapi import APIRouter, Depends, File, UploadFile, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.core.database import get_db
from app.core.errors import NotFoundError
from app.models.report import Report, LabResult, ReportStatus
from app.schemas.report import LabResultOut, ReportDetail, ReportSummary, UploadResponse
from app.services.extraction_service import ExtractionService

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/upload", response_model=UploadResponse, status_code=201)
def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    data = file.file.read()
    service = ExtractionService(get_settings(), db)
    processed = service.process_upload(
        filename=file.filename or "report",
        content_type=file.content_type or "",
        data=data,
    )
    return UploadResponse(
        report_id=processed.report_id,
        status="processed",
        report_date=processed.report_date,
        tests_extracted=processed.tests_extracted,
    )


@router.get("", response_model=list[ReportSummary])
def list_reports(db: Session = Depends(get_db)):
    counts = (
        select(LabResult.report_id, func.count(LabResult.id).label("count"))
        .group_by(LabResult.report_id)
        .subquery()
    )
    stmt = (
        select(Report, counts.c.count)
        .outerjoin(counts, counts.c.report_id == Report.id)
        .order_by(Report.created_at.desc(), Report.id.desc())
    )
    rows = db.execute(stmt).all()
    return [
        ReportSummary(
            id=report.id,
            original_filename=report.original_filename,
            mime_type=report.mime_type,
            report_date=report.report_date,
            status=report.status.value,
            tests_count=count or 0,
            created_at=report.created_at,
        )
        for report, count in rows
    ]


@router.get("/{report_id}", response_model=ReportDetail)
def get_report(report_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Report)
        .where(Report.id == report_id)
        .options(selectinload(Report.results))
    )
    report = db.execute(stmt).scalar_one_or_none()
    if report is None:
        raise NotFoundError("Report not found.")
    return ReportDetail(
        id=report.id,
        original_filename=report.original_filename,
        mime_type=report.mime_type,
        report_date=report.report_date,
        status=report.status.value,
        created_at=report.created_at,
        raw_text=report.raw_text,
        result_count=len(report.results),
        results=report.results,
    )


@router.get("/{report_id}/results", response_model=list[LabResultOut])
def get_report_results(
    report_id: int,
    test_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    report = db.get(Report, report_id)
    if report is None:
        raise NotFoundError("Report not found.")
    if test_name:
        return [result for result in report.results if result.test_name_normalized.casefold() == test_name.strip().casefold()]
    return report.results