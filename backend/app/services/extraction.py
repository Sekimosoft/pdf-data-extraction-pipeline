import os
import tempfile

from fastapi import UploadFile

from app.config import Settings
from app.extraction.invoice_parser import is_invoice_candidate, parse_invoice_text
from app.extraction.pdf_reader import PdfReadError, extract_text_from_pdf
from app.fixtures import sample_invoice_path
from app.models.schemas import (
    ExtractResponse,
    Locale,
    ResultMode,
    TextPreview,
    ValidationIssue,
)
from app.validation.rules import MESSAGES, validate_extraction

ALLOWED_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream"}

NOTICE_MESSAGES: dict[Locale, str] = {
    "en": "Text extraction succeeded, but this document is not a supported invoice template.",
    "ja": "テキスト抽出には成功しましたが、この文書は対応している請求書形式ではありません。",
}

PREVIEW_MAX_CHARS = 600


class ExtractionService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def extract(self, file: UploadFile, locale: Locale) -> ExtractResponse:
        self._validate_upload(file)
        tmp_path: str | None = None
        try:
            content = await file.read()
            if len(content) > self.settings.max_file_size_bytes:
                raise ValueError(f"File exceeds {self.settings.max_file_size_mb} MB limit")
            if len(content) == 0:
                raise ValueError("Empty file")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            pdf_result = extract_text_from_pdf(tmp_path, self.settings.max_pdf_pages)
            if not pdf_result.text:
                msg = MESSAGES.get(locale, MESSAGES["en"])["no_text"]
                return ExtractResponse(
                    success=False,
                    resultMode="extraction_error",
                    validationIssues=[ValidationIssue(field="_file", message=msg, severity="error")],
                    locale=locale,
                )

            if not is_invoice_candidate(pdf_result.text):
                return self._text_preview_response(pdf_result.text, pdf_result.page_count, locale)

            parsed = parse_invoice_text(pdf_result.text)
            document, issues = validate_extraction(parsed, locale)

            if document.validationState == "error" and document.confidence < 0.35:
                return self._text_preview_response(pdf_result.text, pdf_result.page_count, locale)

            return ExtractResponse(
                success=document.validationState != "error",
                resultMode="invoice_structured",
                data=document,
                validationIssues=issues,
                locale=locale,
            )
        except PdfReadError as exc:
            return ExtractResponse(
                success=False,
                resultMode="extraction_error",
                validationIssues=[ValidationIssue(field="_file", message=str(exc), severity="error")],
                locale=locale,
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            await file.close()

    def _text_preview_response(self, text: str, page_count: int, locale: Locale) -> ExtractResponse:
        preview = text[:PREVIEW_MAX_CHARS]
        if len(text) > PREVIEW_MAX_CHARS:
            preview += "…"
        return ExtractResponse(
            success=True,
            resultMode="text_preview",
            textPreview=TextPreview(
                pageCount=page_count,
                characterCount=len(text),
                textPreview=preview,
            ),
            notice=NOTICE_MESSAGES[locale],
            locale=locale,
        )

    def _validate_upload(self, file: UploadFile) -> None:
        filename = (file.filename or "").lower()
        if not filename.endswith(".pdf"):
            raise ValueError("Only PDF files are supported")
        content_type = (file.content_type or "").lower()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Invalid file type — PDF required")


def get_sample_pdf_bytes(locale: Locale = "en") -> bytes:
    path = sample_invoice_path(locale)
    if not path.exists():
        from app.fixtures.generate_fixtures import generate_en_invoice, generate_ja_invoice

        if locale == "ja":
            generate_ja_invoice()
        else:
            generate_en_invoice()
    return path.read_bytes()
