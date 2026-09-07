from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import NotFoundError, InvalidCorrectionError
from app.models.report import LabResult
from app.schemas.report import CorrectionRequest, LabResultOut


router = APIRouter(prefix="/api/reports", tags=["corrections"])


@router.patch("/{report_id}/results/{result_id}", response_model=LabResultOut)
def correct_result(report_id: int, result_id: int, request: CorrectionRequest, db: Session = Depends(get_db)):
    result = db.query(LabResult).filter(LabResult.id == result_id, LabResult.report_id == report_id).first()
    if result is None:
        raise NotFoundError()
    if request.value_numeric is None and not (request.value_text or "").strip():
        raise InvalidCorrectionError()
    if result.value_numeric_original is None and result.value_text_original is None:
        result.value_numeric_original = result.value_numeric
        result.value_text_original = result.value_text
    result.value_numeric = request.value_numeric
    result.value_text = request.value_text.strip() if request.value_text else None
    result.correction_note = request.reason
    result.corrected_at = datetime.utcnow()
    db.commit()
    db.refresh(result)
    return result