from fastapi import APIRouter, Depends, File, Form, UploadFile, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.core.database import get_db
from app.core.errors import NotFoundError
from app.models.report import Report, LabResult, ReportStatus
from app.models.patient import Patient
from app.schemas.report import LabResultOut, ReportDetail, ReportSummary, UploadResponse
from app.services.extraction_service import ExtractionService

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/upload", response_model=UploadResponse, status_code=201)
def upload_report(
    file: UploadFile = File(...),
    patient_name: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    data = file.file.read()
    service = ExtractionService(get_settings(), db)
    processed = service.process_upload(
        filename=file.filename or "report",
        content_type=file.content_type or "",
        data=data,
        patient_name=patient_name,
    )
    report = db.query(Report).filter(Report.id == processed.report_id).first()
    return UploadResponse(
        report_id=processed.report_id,
        patient_id=report.patient_id,
        patient_name=report.patient.name,
        status="processed",
        report_date=processed.report_date,
        tests_extracted=processed.tests_extracted,
    )


@router.get("", response_model=list[ReportSummary])
def list_reports(patient_id: int | None = Query(default=None, gt=0), db: Session = Depends(get_db)):
    counts = (
        select(
            LabResult.report_id,
            func.count(LabResult.id).label("count"),
            func.sum(case((LabResult.data_quality != "good", 1), else_=0)).label("attention_count"),
        )
        .group_by(LabResult.report_id)
        .subquery()
    )
    stmt = (
        select(Report, counts.c.count, counts.c.attention_count)
        .outerjoin(counts, counts.c.report_id == Report.id)
        .where(Report.user_id == 1)
        .order_by(Report.created_at.desc(), Report.id.desc())
    )
    if patient_id is not None:
        stmt = stmt.where(Report.patient_id == patient_id)
    rows = db.execute(stmt).all()
    return [
        ReportSummary(
            id=report.id,
            patient_id=report.patient_id,
            patient_name=report.patient.name,
            original_filename=report.original_filename,
            mime_type=report.mime_type,
            report_date=report.report_date,
            status=report.status.value,
            tests_count=count or 0,
            attention_count=attention_count or 0,
            created_at=report.created_at,
        )
        for report, count, attention_count in rows
    ]


@router.get("/{report_id}", response_model=ReportDetail)
def get_report(report_id: int, patient_id: int | None = Query(default=None, gt=0), db: Session = Depends(get_db)):
    stmt = (
        select(Report)
        .where(Report.id == report_id, Report.user_id == 1)
        .options(selectinload(Report.results))
    )
    if patient_id is not None:
        stmt = stmt.where(Report.patient_id == patient_id)
    report = db.execute(stmt).scalar_one_or_none()
    if report is None:
        raise NotFoundError()
    return ReportDetail(
        id=report.id,
        patient_id=report.patient_id,
        patient_name=report.patient.name,
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
    patient_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == 1).first()
    if report is None or (patient_id is not None and report.patient_id != patient_id):
        raise NotFoundError()
    if test_name:
        return [result for result in report.results if result.test_name_normalized.casefold() == test_name.strip().casefold()]
    return report.results