from app.core.errors import CorruptedFileError, ExtractionEmptyError

try:
    import pymupdf as _pymupdf
except ImportError:  # pragma: no cover
    import fitz as _pymupdf


class PDFExtractor:
    """Extracts raw text from PDF reports using PyMuPDF."""

    source_type = "pdf"
    extraction_method = "pymupdf"

    @staticmethod
    def extract(data: bytes) -> dict:
        try:
            document = _pymupdf.open(stream=data, filetype="pdf")
        except Exception:
            raise CorruptedFileError()

        pages = []
        for page in document:
            pages.append(
                {
                    "page_index": page.number,
                    "text": page.get_text("text"),
                }
            )

        document.close()

        raw = "\n\n".join(page["text"] for page in pages if page["text"].strip()).strip()
        if not raw:
            raise ExtractionEmptyError()

        return {
            "source_type": PDFExtractor.source_type,
            "raw_text": raw,
            "extraction_method": PDFExtractor.extraction_method,
            "pages": pages,
        }