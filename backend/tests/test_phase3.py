import sys
from pathlib import Path
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.core.database import Base
from app.core.database import get_db
from app.core.config import Settings
from app.main import create_app
from app.models import LabResult, Patient, Report, ReportStatus, User
from app.schemas.extraction import ParserResult
from app.services.ingestion.lab_parser import DeterministicParser
from app.services.ingestion.normalization import normalize_test_name, normalize_unit
from app.services.ingestion.reference_ranges import parse_reference_range
from app.services.ingestion.validators import finalize_results
from app.services.extraction_service import ExtractionService


def test_test_name_and_unit_normalization():
    assert normalize_test_name(" HbA1C ") == "HbA1c"
    assert normalize_test_name("Unlisted test") == "Unlisted test"
    assert normalize_unit("MG / dL") == "mg/dL"
    assert normalize_unit(None) is None
    assert normalize_unit("mg/dL") == "mg/dL"


def test_reference_range_formats_preserve_text():
    assert parse_reference_range("4.0 to 5.6").model_dump() == {
        "low": 4.0,
        "high": 5.6,
        "text": "4.0 to 5.6",
    }
    assert parse_reference_range("< 100").high == 100
    assert parse_reference_range("> 40").low == 40
    assert parse_reference_range("not available").low is None
    assert parse_reference_range("not available").text == "not available"
    assert parse_reference_range(None) is None


def test_quality_and_duplicate_conflict_classification_preserves_rows():
    rows = finalize_results(
        [
            ParserResult(test_name_original="Glucose", value_numeric=95, unit="mg / dL"),
            ParserResult(test_name_original="Glucose", value_numeric=110, unit="MG/DL"),
            ParserResult(test_name_original="Hemoglobin", value_numeric=13.8, unit="g/dL", reference_range=parse_reference_range("13-17")),
            ParserResult(test_name_original="Protein", value_text="Positive", unit=None),
        ]
    )
    assert len(rows) == 4
    assert rows[0].data_quality == "conflicting_values"
    assert rows[1].data_quality == "conflicting_values"
    assert rows[2].data_quality == "good"
    assert rows[3].data_quality == "missing_unit"


def test_identical_duplicates_are_preserved():
    rows = finalize_results(
        [
            ParserResult(test_name_original="Glucose", value_numeric=95, unit="mg/dL"),
            ParserResult(test_name_original="Glucose", value_numeric=95, unit="mg / dL"),
        ]
    )
    assert len(rows) == 2
    assert all(row.data_quality == "duplicate_test" for row in rows)


def test_qualitative_parser_value_is_not_forced_numeric():
    result = DeterministicParser().parse("Protein Positive").tests[0]
    assert result.value_numeric is None
    assert result.value_text == "Positive"


def test_parser_supports_worded_ranges_and_spaced_units():
    result = DeterministicParser().parse("Glucose 95 mg / dL 70 to 100").tests[0]
    assert result.value_numeric == 95
    assert result.unit == "mg/dL"
    assert result.reference_range.low == 70
    assert result.reference_range.high == 100


def test_report_user_result_relationship_and_delete_cascade():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    user = User(display_name="Demo User")
    report = Report(
        user=user,
        original_filename="sample.pdf",
        mime_type="application/pdf",
        content_hash="a" * 64,
        raw_text="Glucose 95 mg/dL",
        status=ReportStatus.PROCESSED,
    )
    report.results.append(
        LabResult(
            test_name_original="Glucose",
            test_name_normalized="Glucose",
            value_numeric=95,
            unit="mg/dL",
            raw_text="Glucose 95 mg/dL",
            confidence="high",
            data_quality="missing_reference_range",
        )
    )
    session.add(report)
    session.commit()
    report_id = report.id
    result_id = report.results[0].id
    assert session.get(Report, report_id).user.display_name == "Demo User"
    assert session.get(LabResult, result_id).report.id == report_id
    session.delete(session.get(Report, report_id))
    session.commit()
    assert session.get(LabResult, result_id) is None


def test_report_api_list_detail_results_filter_and_not_found():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    report = Report(
        user=User(display_name="Demo User"),
        original_filename="panel.pdf",
        mime_type="application/pdf",
        content_hash="b" * 64,
        raw_text="Glucose 95 mg/dL",
        status=ReportStatus.PROCESSED,
    )
    report.results.extend([
        LabResult(
            test_name_original="A1C",
            test_name_normalized="HbA1c",
            value_numeric=5.9,
            unit="%",
            raw_text="A1C 5.9 %",
            confidence="high",
            data_quality="good",
        ),
        LabResult(
            test_name_original="Glucose",
            test_name_normalized="Glucose",
            value_numeric=95,
            unit="mg/dL",
            raw_text="Glucose 95 mg/dL",
            confidence="high",
            data_quality="missing_reference_range",
        ),
    ])
    session.add(report)
    session.commit()

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    assert client.get("/api/reports").json()[0]["tests_count"] == 2
    detail = client.get(f"/api/reports/{report.id}")
    assert detail.status_code == 200
    assert detail.json()["result_count"] == 2
    filtered = client.get(f"/api/reports/{report.id}/results?test_name=HbA1c")
    assert [item["test_name_normalized"] for item in filtered.json()] == ["HbA1c"]
    missing = client.get("/api/reports/999")
    assert missing.status_code == 404
    assert missing.json() == {"error": {"code": "REPORT_NOT_FOUND", "message": "We couldn't find that report."}}
    corrected = client.patch(f"/api/reports/{report.id}/results/{report.results[0].id}", json={"value_numeric": 6.1, "reason": "Checked against source document"})
    assert corrected.status_code == 200
    assert corrected.json()["value_numeric"] == 6.1
    assert corrected.json()["value_numeric_original"] == 5.9
    assert corrected.json()["correction_note"] == "Checked against source document"


def test_duplicate_content_hash_can_be_uploaded_as_a_new_report():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    duplicate_data = (Path(__file__).parents[1] / "sample_reports" / "normal_report.pdf").read_bytes()
    patient = Patient(user=User(display_name="Demo User"), name="Alex Morgan", normalized_name="alex morgan")
    session.add(patient)
    session.commit()

    service = ExtractionService(Settings(), session)
    first = service.process_upload("copy.pdf", "application/pdf", duplicate_data, patient_name="Alex Morgan")
    second = service.process_upload("copy-again.pdf", "application/pdf", duplicate_data, patient_name="Alex Morgan")

    assert first.report_id != second.report_id
    reports = session.query(Report).all()
    assert len(reports) == 2
    assert reports[0].content_hash == reports[1].content_hash
