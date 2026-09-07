import re
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientOut


DEMO_USER_ID = 1
router = APIRouter(prefix="/api/patients", tags=["patients"])


def normalize_patient_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).casefold()


@router.get("", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).filter(Patient.user_id == DEMO_USER_ID).order_by(Patient.name.asc()).all()


@router.post("", response_model=PatientOut, status_code=201)
def create_patient(request: PatientCreate, db: Session = Depends(get_db)):
    normalized = normalize_patient_name(request.name)
    existing = db.query(Patient).filter(Patient.user_id == DEMO_USER_ID, Patient.normalized_name == normalized).first()
    if existing:
        return existing
    patient = Patient(user_id=DEMO_USER_ID, name=request.name.strip(), normalized_name=normalized, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient