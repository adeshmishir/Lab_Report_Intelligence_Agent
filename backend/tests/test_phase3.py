import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.schemas.extraction import ParserResult
from app.services.ingestion.lab_parser import DeterministicParser
from app.services.ingestion.normalization import normalize_test_name, normalize_unit
from app.services.ingestion.reference_ranges import parse_reference_range
from app.services.ingestion.validators import finalize_results


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
