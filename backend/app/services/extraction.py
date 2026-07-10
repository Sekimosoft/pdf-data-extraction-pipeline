import os
import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.config import Settings
from app.extraction.invoice_parser import parse_invoice_text
from app.extraction.pdf_reader import PdfReadError, extract_text_from_pdf
from app.models.schemas import ExtractResponse, Locale, ValidationIssue
from app.validation.rules import MESSAGES, validate_extraction

ALLOWED_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream"}


class ExtractionService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def extract(self, file: UploadFile, locale: Locale) -> ExtractResponse:
        self._validate_upload(file)
        suffix = ".pdf"
        tmp_path: str | None = None
        try:
            content = await file.read()
            if len(content) > self.settings.max_file_size_bytes:
                raise ValueError(f"File exceeds {self.settings.max_file_size_mb} MB limit")
            if len(content) == 0:
                raise ValueError("Empty file")

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            text = extract_text_from_pdf(tmp_path, self.settings.max_pdf_pages)
            if not text:
                msg = MESSAGES.get(locale, MESSAGES["en"])["no_text"]
                return ExtractResponse(
                    success=False,
                    validationIssues=[
                        ValidationIssue(field="_file", message=msg, severity="error"),
                    ],
                    locale=locale,
                )

            parsed = parse_invoice_text(text)
            document, issues = validate_extraction(parsed, locale)
            return ExtractResponse(
                success=document.validationState != "error",
                data=document,
                validationIssues=issues,
                locale=locale,
            )
        except PdfReadError as exc:
            return ExtractResponse(
                success=False,
                validationIssues=[
                    ValidationIssue(field="_file", message=str(exc), severity="error"),
                ],
                locale=locale,
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            await file.close()

    def _validate_upload(self, file: UploadFile) -> None:
        filename = (file.filename or "").lower()
        if not filename.endswith(".pdf"):
            raise ValueError("Only PDF files are supported")
        content_type = (file.content_type or "").lower()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Invalid file type — PDF required")


def get_sample_pdf_bytes() -> bytes:
    fixture = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "sample_invoice.pdf"
    return fixture.read_bytes()
