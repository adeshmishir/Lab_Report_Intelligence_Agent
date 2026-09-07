from datetime import date, datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings
from app.core.database import Base, get_db
from app.main import create_app
from app.models import LabResult, Report, ReportStatus, User


def make_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    session = factory()
    user = User(display_name="Demo User")
    report = Report(
        user=user,
        original_filename="panel.pdf",
        mime_type="application/pdf",
        report_date=date(2026, 8, 12),
        raw_text="HbA1c: 5.9 % (4.0 - 5.6)",
        status=ReportStatus.PROCESSED,
        created_at=datetime(2026, 8, 12),
    )
    report.results.extend([
        LabResult(
            test_name_original="A1C",
            test_name_normalized="HbA1c",
            value_numeric=5.9,
            unit="%",
            reference_text="4.0 - 5.6",
            raw_text="A1C: 5.9 % (4.0 - 5.6)",
            confidence="high",
            data_quality="good",
        ),
    ])
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
    return TestClient(app)


def test_ask_returns_grounded_latest_result_and_citation():
    response = make_client().post("/api/ask", json={"question": "What was my latest HbA1c?"})
    assert response.status_code == 200
    payload = response.json()
    assert "5.9" in payload["answer"]
    assert payload["citations"][0]["test_name"] == "HbA1c"
    assert payload["citations"][0]["report_id"] == 1


def test_ask_resolves_obvious_test_aliases():
    response = make_client().post("/api/ask", json={"question": "What was my latest A1C?"})
    assert "5.9" in response.json()["answer"]


def test_ask_handles_safety_and_missing_test_name():
    safety = make_client().post("/api/ask", json={"question": "Can you diagnose my disease?"}).json()
    assert safety["safety_notice"]
    assert not safety["citations"]
    unclear = make_client().post("/api/ask", json={"question": "What should I do?"}).json()
    assert "include a test name" in unclear["answer"]


def test_ask_supports_report_scope():
    response = make_client().post("/api/ask", json={"question": "Show HbA1c trend", "report_id": 999})
    assert "include a test name" in response.json()["answer"]