import re
from typing import Any

FIELD_PATTERN_GROUPS: dict[str, list[str]] = {
    "documentType": [
        r"Document Type:\s*(.+)",
        r"書類種別[:：]\s*(.+)",
    ],
    "invoiceNumber": [
        r"Invoice Number:\s*(.+)",
        r"請求書番号[:：]\s*(.+)",
    ],
    "issueDate": [
        r"Issue Date:\s*(\d{4}-\d{2}-\d{2})",
        r"発行日[:：]\s*(\d{4}-\d{2}-\d{2})",
    ],
    "dueDate": [
        r"Due Date:\s*(\d{4}-\d{2}-\d{2})",
        r"支払期限[:：]\s*(\d{4}-\d{2}-\d{2})",
    ],
    "vendorName": [
        r"Vendor:\s*(.+)",
        r"発行元[:：]\s*(.+)",
    ],
    "customerName": [
        r"Customer:\s*(.+)",
        r"請求先[:：]\s*(.+)",
    ],
    "subtotal": [
        r"Subtotal:\s*([\d,]+\.?\d*)",
        r"小計[:：]\s*([\d,]+\.?\d*)",
    ],
    "tax": [
        r"Tax:\s*([\d,]+\.?\d*)",
        r"消費税[:：]\s*([\d,]+\.?\d*)",
    ],
    "total": [
        r"(?<!Sub)Total:\s*([\d,]+\.?\d*)",
        r"合計[:：]\s*([\d,]+\.?\d*)",
    ],
    "currency": [
        r"Currency:\s*([A-Z]{3})",
        r"通貨[:：]\s*([A-Z]{3})",
    ],
}


def _parse_amount(raw: str) -> float:
    return float(raw.replace(",", ""))


def is_invoice_candidate(text: str) -> bool:
    upper = text.upper()
    return "INVOICE" in upper or "請求書" in text


def parse_invoice_text(text: str) -> dict[str, Any]:
    """Rule-based parser for V1 synthetic invoice templates only."""
    if not is_invoice_candidate(text):
        return {"documentType": None}

    result: dict[str, Any] = {}
    for field, patterns in FIELD_PATTERN_GROUPS.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE if field != "total" else 0)
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
            break

    if result.get("documentType") is None:
        result["documentType"] = "invoice"

    return result
