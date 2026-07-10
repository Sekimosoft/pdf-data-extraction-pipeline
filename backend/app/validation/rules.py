from datetime import date
from typing import Any

from app.models.schemas import ExtractedDocument, Locale, ValidationIssue, ValidationState

TRACKED_FIELDS = [
    "documentType",
    "invoiceNumber",
    "issueDate",
    "dueDate",
    "vendorName",
    "customerName",
    "subtotal",
    "tax",
    "total",
    "currency",
]

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "missing_invoice_number": "Invoice number is required",
        "missing_issue_date": "Issue date is required",
        "missing_total": "Total amount is required",
        "invalid_date": "Date must be ISO format YYYY-MM-DD",
        "negative_amount": "Amount must be non-negative",
        "total_mismatch": "Total does not match subtotal + tax",
        "missing_due_date": "Due date is missing — manual review recommended",
        "low_confidence": "Few fields extracted — document may be outside V1 template",
        "no_text": "No extractable text — scanned PDFs are not supported in V1",
    },
    "ja": {
        "missing_invoice_number": "請求書番号は必須です",
        "missing_issue_date": "発行日は必須です",
        "missing_total": "合計金額は必須です",
        "invalid_date": "日付は YYYY-MM-DD 形式である必要があります",
        "negative_amount": "金額は0以上である必要があります",
        "total_mismatch": "合計が小計+税と一致しません",
        "missing_due_date": "支払期日がありません — 手動確認を推奨します",
        "low_confidence": "抽出フィールドが少ない — V1テンプレート外の可能性があります",
        "no_text": "抽出可能なテキストがありません — V1ではスキャンPDF非対応です",
    },
}


def _msg(locale: Locale, key: str) -> str:
    return MESSAGES.get(locale, MESSAGES["en"])[key]


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def compute_confidence(parsed: dict[str, Any]) -> float:
    filled = sum(1 for field in TRACKED_FIELDS if parsed.get(field) not in (None, ""))
    return round(filled / len(TRACKED_FIELDS), 2)


def validate_extraction(parsed: dict[str, Any], locale: Locale = "en") -> tuple[ExtractedDocument, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    confidence = compute_confidence(parsed)

    if not parsed.get("invoiceNumber"):
        issues.append(
            ValidationIssue(field="invoiceNumber", message=_msg(locale, "missing_invoice_number"), severity="error")
        )
    if not parsed.get("issueDate"):
        issues.append(
            ValidationIssue(field="issueDate", message=_msg(locale, "missing_issue_date"), severity="error")
        )
    elif _parse_iso_date(parsed.get("issueDate")) is None:
        issues.append(
            ValidationIssue(field="issueDate", message=_msg(locale, "invalid_date"), severity="error")
        )

    if parsed.get("dueDate") and _parse_iso_date(parsed.get("dueDate")) is None:
        issues.append(
            ValidationIssue(field="dueDate", message=_msg(locale, "invalid_date"), severity="error")
        )
    elif not parsed.get("dueDate"):
        issues.append(
            ValidationIssue(field="dueDate", message=_msg(locale, "missing_due_date"), severity="warning")
        )

    for amount_field in ("subtotal", "tax", "total"):
        amount = parsed.get(amount_field)
        if amount is not None and amount < 0:
            issues.append(
                ValidationIssue(
                    field=amount_field,
                    message=_msg(locale, "negative_amount"),
                    severity="error",
                )
            )

    if parsed.get("total") is None:
        issues.append(
            ValidationIssue(field="total", message=_msg(locale, "missing_total"), severity="error")
        )

    subtotal = parsed.get("subtotal")
    tax = parsed.get("tax")
    total = parsed.get("total")
    if subtotal is not None and tax is not None and total is not None:
        if round(subtotal + tax, 2) != round(total, 2):
            issues.append(
                ValidationIssue(field="total", message=_msg(locale, "total_mismatch"), severity="warning")
            )

    if confidence < 0.5:
        issues.append(
            ValidationIssue(field="_document", message=_msg(locale, "low_confidence"), severity="warning")
        )

    has_error = any(i.severity == "error" for i in issues)
    has_warning = any(i.severity == "warning" for i in issues)
    if has_error:
        state: ValidationState = "error"
    elif has_warning:
        state = "warning"
    else:
        state = "valid"

    document = ExtractedDocument(
        documentType=parsed.get("documentType"),
        invoiceNumber=parsed.get("invoiceNumber"),
        issueDate=parsed.get("issueDate"),
        dueDate=parsed.get("dueDate"),
        vendorName=parsed.get("vendorName"),
        customerName=parsed.get("customerName"),
        subtotal=parsed.get("subtotal"),
        tax=parsed.get("tax"),
        total=parsed.get("total"),
        currency=parsed.get("currency"),
        confidence=confidence,
        validationState=state,
    )
    return document, issues
