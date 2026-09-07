import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.services.ingestion.lab_parser import DeterministicParser


def test_parser_extracts_multiline_table_rows_and_adjacent_report_date():
    extraction = DeterministicParser().parse(
        "Report Date\n24 Jul 2026\nTest Name\nResult\nUnit\nReference Range\n"
        "Hemoglobin\n13.8\ng/dL\n13.0 - 17.0"
    )
    assert extraction.report_date == "2026-07-24"
    assert len(extraction.tests) == 1
    assert extraction.tests[0].test_name_original == "Hemoglobin"
    assert extraction.tests[0].value_numeric == 13.8
    assert extraction.tests[0].reference_range.low == 13.0


def test_parser_extracts_patient_name_from_labeled_report_header():
    extraction = DeterministicParser().parse(
        "Patient Name: Alex Morgan\nReport Date: 2026-07-24\nGlucose 95 mg/dL 70 - 100"
    )

    assert extraction.patient_name == "Alex Morgan"


def test_parser_marks_pre_tagged_critical_result():
    result = DeterministicParser().parse("Troponin 0.8 ng/mL 0.0 - 0.04 [CRITICAL]").tests[0]
    assert result.critical is True