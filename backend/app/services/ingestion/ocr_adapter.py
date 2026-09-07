import io

import numpy as np
from PIL import Image

from app.core.errors import ExtractionEmptyError, OcrError


class OCRAdapter:
    """Isolated OCR layer so the implementation can be swapped later.

    The rest of the pipeline only depends on ``OCRAdapter.extract``.
    """

    source_type = "image"
    extraction_method = "rapidocr"

    def __init__(self, backend: str = "rapidocr"):
        self.backend = backend
        self._engine = None

    def _load_engine(self):
        if self._engine is not None:
            return self._engine
        if self.backend == "rapidocr":
            try:
                from rapidocr_onnxruntime import RapidOCR
            except ImportError as exc:  # pragma: no cover
                raise OcrError() from exc
            self._engine = RapidOCR()
        else:
            raise OcrError()
        return self._engine

    def extract(self, data: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(data))
            image.verify()
            image = Image.open(io.BytesIO(data))
        except Exception:
            raise OcrError()

        # Convert to RGB/RGBA so every input (incl. L/P modes) reaches OCR fine.
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        array = np.asarray(image)

        try:
            engine = self._load_engine()
            result, _ = engine(array)
        except OcrError:
            raise
        except Exception:
            raise OcrError()

        if not result:
            raise ExtractionEmptyError()

        region_texts = [(line[1], line[0][0][1]) for line in result]  # text, top-y
        region_texts.sort(key=lambda item: (item[1], 0))
        raw = "\n".join(text.strip() for text, _ in region_texts if text.strip()).strip()

        if not raw:
            raise ExtractionEmptyError()

        return {
            "source_type": OCRAdapter.source_type,
            "raw_text": raw,
            "extraction_method": OCRAdapter.extraction_method,
            "pages": [{"page_index": 0, "text": raw}],
        }