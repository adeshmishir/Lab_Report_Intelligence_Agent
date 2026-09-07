import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.core.config import Settings
from app.services.ingestion.lab_parser import parse_raw_text


def test_auto_mode_falls_back_when_llm_extraction_fails(monkeypatch):
    class FailedParser:
        def parse(self, raw_text):
            from app.core.errors import ParserError
            raise ParserError()

    monkeypatch.setattr("app.services.ingestion.lab_parser.build_parser", lambda settings: FailedParser())
    extraction = parse_raw_text("Glucose 95 mg/dL 70-99", Settings(EXTRACTION_MODE="auto"))
    assert extraction.tests[0].value_numeric == 95


def test_explicit_llm_mode_still_surfaces_provider_failure(monkeypatch):
    class FailedParser:
        def parse(self, raw_text):
            from app.core.errors import ParserError
            raise ParserError()

    monkeypatch.setattr("app.services.ingestion.lab_parser.build_parser", lambda settings: FailedParser())
    import pytest
    from app.core.errors import ParserError
    with pytest.raises(ParserError):
        parse_raw_text("Glucose 95 mg/dL 70-99", Settings(EXTRACTION_MODE="llm"))