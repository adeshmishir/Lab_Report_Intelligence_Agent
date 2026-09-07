class LabLensError(Exception):
    """Base class for all application errors."""
    code = "INTERNAL_ERROR"
    status_code = 500
    message = "Something went wrong."

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class UnsupportedFileTypeError(LabLensError):
    code = "UNSUPPORTED_FILE_TYPE"
    status_code = 400
    message = "Please upload a PDF, JPG, or PNG report."


class FileTooLargeError(LabLensError):
    code = "FILE_TOO_LARGE"
    status_code = 413
    message = "The uploaded file is too large."


class EmptyFileError(LabLensError):
    code = "EMPTY_FILE"
    status_code = 400
    message = "The uploaded file is empty."


class CorruptedFileError(LabLensError):
    code = "CORRUPTED_FILE"
    status_code = 422
    message = "We couldn't read this file. Please try another sample report."


class OcrError(LabLensError):
    code = "OCR_FAILED"
    status_code = 422
    message = "We couldn't read the text in this image. Please try another sample report."


class ExtractionEmptyError(LabLensError):
    code = "NO_TEXT_EXTRACTED"
    status_code = 422
    message = "We couldn't process this report. Please try another sample report."


class ParserError(LabLensError):
    code = "PARSING_FAILED"
    status_code = 422
    message = "We couldn't process this report. Please try another sample report."


class NotFoundError(LabLensError):
    code = "REPORT_NOT_FOUND"
    status_code = 404
    message = "We couldn't find that report."


class ProcessingFailedError(LabLensError):
    code = "PROCESSING_FAILED"
    status_code = 422
    message = "We couldn't process this report."


class DuplicateReportError(LabLensError):
    code = "DUPLICATE_REPORT"
    status_code = 409
    message = "This report has already been uploaded."


class InvalidCorrectionError(LabLensError):
    code = "INVALID_CORRECTION"
    status_code = 422
    message = "Enter a numeric or text value for the correction."