import re
from typing import Any

FIELD_PATTERNS: dict[str, re.Pattern[str]] = {
    "documentType": re.compile(r"Document Type:\s*(.+)", re.IGNORECASE),
    "invoiceNumber": re.compile(r"Invoice Number:\s*(.+)", re.IGNORECASE),
    "issueDate": re.compile(r"Issue Date:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    "dueDate": re.compile(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    "vendorName": re.compile(r"Vendor:\s*(.+)", re.IGNORECASE),
    "customerName": re.compile(r"Customer:\s*(.+)", re.IGNORECASE),
    "subtotal": re.compile(r"Subtotal:\s*([\d,]+\.?\d*)", re.IGNORECASE),
    "tax": re.compile(r"Tax:\s*([\d,]+\.?\d*)", re.IGNORECASE),
    "total": re.compile(r"Total:\s*([\d,]+\.?\d*)", re.IGNORECASE),
    "currency": re.compile(r"Currency:\s*([A-Z]{3})", re.IGNORECASE),
}


def _parse_amount(raw: str) -> float:
    return float(raw.replace(",", ""))


def parse_invoice_text(text: str) -> dict[str, Any]:
    """Rule-based parser for V1 synthetic invoice template only."""
    if "INVOICE" not in text.upper():
        return {"documentType": None}

    result: dict[str, Any] = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = pattern.search(text)
        if not match:
            continue
        value = match.group(1).strip()
        if field in {"subtotal", "tax", "total"}:
            try:
                result[field] = _parse_amount(value)
            except ValueError:
                continue
        else:
            result[field] = value

    if result.get("documentType") is None and "INVOICE" in text.upper():
        result["documentType"] = "invoice"

    return result
