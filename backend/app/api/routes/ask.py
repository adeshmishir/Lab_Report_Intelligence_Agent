from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.qa_service import AskService


router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask", response_model=AskResponse)
def ask_lab_lens(
    request: AskRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    return AskService(settings, db).answer(request.question, request.report_id)