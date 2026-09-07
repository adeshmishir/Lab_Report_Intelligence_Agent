from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.report import LabResult, Report, ReportStatus


router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("")
def get_trends(
    test_name: str | None = Query(default=None),
    patient_id: int = Query(default=1, gt=0),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Report, LabResult)
        .join(LabResult, LabResult.report_id == Report.id)
        .where(Report.user_id == 1, Report.patient_id == patient_id, Report.status == ReportStatus.PROCESSED)
        .order_by(Report.report_date.asc(), Report.id.asc(), LabResult.id.asc())
    )
    if test_name:
        stmt = stmt.where(LabResult.test_name_normalized.ilike(test_name.strip()))

    trends: dict[str, list[dict]] = {}
    for report, result in db.execute(stmt).all():
        if result.value_numeric is None:
            continue
        trends.setdefault(result.test_name_normalized, []).append(
            {
                "report_id": report.id,
                "result_id": result.id,
                "date": report.report_date.isoformat() if report.report_date else None,
                "value": result.value_numeric,
                "unit": result.unit,
                "data_quality": result.data_quality.value,
            }
        )
    return {"tests": sorted(trends), "data": trends}