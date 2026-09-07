from app.core.errors import OcrError
from app.schemas.extraction import ExtractedDocument

from app.services.ingestion.pdf_extractor import PDFExtractor
from app.services.ingestion.ocr_adapter import OCRAdapter
from app.services.ingestion.file_validator import ValidatedFile

PDF_MIME = "application/pdf"
IMAGE_MIMES = {"image/jpeg", "image/png"}


class TextExtractor:
    """Dispatches to the right extractor based on the validated file type."""

    def __init__(self, ocr_backend: str = "rapidocr"):
        self.ocr = OCRAdapter(backend=ocr_backend)

    def extract_document(self, file: ValidatedFile) -> ExtractedDocument:
        if file.mime_type == PDF_MIME:
            output = PDFExtractor.extract(file.data)
        elif file.mime_type in IMAGE_MIMES:
            output = self.ocr.extract(file.data)
        else:
            raise OcrError()

        return ExtractedDocument(**output)