import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.services.ingestion.ocr_adapter import OCRAdapter


def test_ocr_retries_preprocessed_variants(monkeypatch):
    adapter = OCRAdapter()
    calls = []

    class FakeEngine:
        def __call__(self, image):
            calls.append(image)
            if len(calls) == 2:
                return [([[0, 0], [10, 0], [10, 10], [0, 10]], "Glucose 95 mg/dL")], None
            return None, None

    monkeypatch.setattr(adapter, "_load_engine", lambda: FakeEngine())
    image_path = Path(__file__).parents[1] / "sample_reports" / "normal_report.png"
    output = adapter.extract(image_path.read_bytes())
    assert "Glucose 95 mg/dL" in output["raw_text"]
    assert len(calls) == 2