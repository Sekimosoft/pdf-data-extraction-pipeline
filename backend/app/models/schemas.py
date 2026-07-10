from typing import Literal

from pydantic import BaseModel, Field


Locale = Literal["en", "ja"]
ValidationState = Literal["valid", "warning", "error"]
ResultMode = Literal["invoice_structured", "text_preview", "extraction_error"]


class ValidationIssue(BaseModel):
    field: str
    message: str
    severity: Literal["error", "warning"] = "error"


class ExtractedDocument(BaseModel):
    documentType: str | None = None
    invoiceNumber: str | None = None
    issueDate: str | None = None
    dueDate: str | None = None
    vendorName: str | None = None
    customerName: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    currency: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    validationState: ValidationState


class TextPreview(BaseModel):
    pageCount: int
    characterCount: int
    textPreview: str
    documentStatus: str = "unsupported_invoice_template"


class ExtractResponse(BaseModel):
    success: bool
    resultMode: ResultMode
    data: ExtractedDocument | None = None
    textPreview: TextPreview | None = None
    notice: str | None = None
    validationIssues: list[ValidationIssue] = Field(default_factory=list)
    provider: str = "rule-based"
    locale: Locale = "en"


class ErrorResponse(BaseModel):
    detail: str
