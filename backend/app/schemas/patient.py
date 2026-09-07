from datetime import datetime

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class PatientOut(BaseModel):
    id: int
    name: str
    normalized_name: str
    created_at: datetime