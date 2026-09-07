import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings
from app.core.database import Base, get_db
from app.main import create_app
from app.models import LabResult, Report, ReportStatus, User


def test_trends_returns_numeric_values_grouped_by_normalized_name():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    session = factory()
    user = User(display_name="Demo User")
    report = Report(
        user=user,
        original_filename="trend.pdf",
        mime_type="application/pdf",
        report_date=date(2026, 8, 12),
        raw_text="A1C 5.9 %",
        status=ReportStatus.PROCESSED,
    )
    report.results.append(LabResult(
        test_name_original="A1C", test_name_normalized="HbA1c", value_numeric=5.9,
        unit="%", raw_text="A1C 5.9 %", confidence="high", data_quality="good",
    ))
    session.add(report)
    session.commit()

    def override_get_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app = create_app(Settings(LLM_API_KEY=""))
    app.dependency_overrides[get_db] = override_get_db
    payload = TestClient(app).get("/api/trends").json()
    assert payload["tests"] == ["HbA1c"]
    assert payload["data"]["HbA1c"][0]["value"] == 5.9