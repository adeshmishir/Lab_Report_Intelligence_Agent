from app.core.errors import (
    EmptyFileError,
    FileTooLargeError,
    UnsupportedFileTypeError,
)

PDF_MIME = "application/pdf"
JPEG_MIME = "image/jpeg"
PNG_MIME = "image/png"
ALLOWED_MIME_TYPES = {PDF_MIME, JPEG_MIME, PNG_MIME}


def detect_mime_from_content(data: bytes) -> str | None:
    """Identify the real file type from magic bytes, not the filename."""
    if data[:5] == b"%PDF-":
        return PDF_MIME
    if data[:3] == b"\xff\xd8\xff":
        return JPEG_MIME
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return PNG_MIME
    return None


class ValidatedFile:
    def __init__(self, filename: str, mime_type: str, size: int, data: bytes):
        self.filename = filename
        self.mime_type = mime_type
        self.size = size
        self.data = data


def validate_file(filename: str, content_type: str, data: bytes, max_size: int) -> ValidatedFile:
    if not data:
        raise EmptyFileError()

    if len(data) > max_size:
        raise FileTooLargeError()

    detected = detect_mime_from_content(data)
    if detected is None:
        raise UnsupportedFileTypeError()

    if content_type and content_type in ALLOWED_MIME_TYPES and content_type != detected:
        raise UnsupportedFileTypeError()

    return ValidatedFile(filename=filename or "report", mime_type=detected, size=len(data), data=data)