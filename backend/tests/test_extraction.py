from app.extraction.invoice_parser import is_invoice_candidate, parse_invoice_text
from app.validation.rules import validate_extraction


def test_parse_en_invoice_text_full() -> None:
    text = """
    INVOICE
    Document Type: invoice
    Invoice Number: INV-EN-2026-0042
    Issue Date: 2026-03-15
    Due Date: 2026-04-15
    Vendor: Acme Supplies Co.
    Customer: Demo Retail Ltd.
    Subtotal: 10,000.00
    Tax: 1,000.00
    Total: 11,000.00
    Currency: USD
    """
    parsed = parse_invoice_text(text)
    assert parsed["invoiceNumber"] == "INV-EN-2026-0042"
    assert parsed["total"] == 11000.0
    assert parsed["currency"] == "USD"


def test_parse_ja_invoice_text_full() -> None:
    text = """
    請求書
    請求書番号: INV-JP-2026-0001
    発行日: 2026-03-15
    支払期限: 2026-04-15
    発行元: デモ商事株式会社
    請求先: サンプル小売店
    小計: 10000.00
    消費税: 1000.00
    合計: 11000.00
    通貨: JPY
    """
    parsed = parse_invoice_text(text)
    assert parsed["invoiceNumber"] == "INV-JP-2026-0001"
    assert parsed["vendorName"] == "デモ商事株式会社"


def test_is_invoice_candidate() -> None:
    assert is_invoice_candidate("INVOICE\nVendor: Demo")
    assert is_invoice_candidate("請求書\n発行元: Demo")
    assert not is_invoice_candidate("Project Brief only")


def test_validation_success() -> None:
    parsed = {
        "documentType": "invoice",
        "invoiceNumber": "INV-1",
        "issueDate": "2026-01-01",
        "dueDate": "2026-02-01",
        "vendorName": "Vendor",
        "customerName": "Customer",
        "subtotal": 100.0,
        "tax": 10.0,
        "total": 110.0,
        "currency": "USD",
    }
    doc, issues = validate_extraction(parsed, "en")
    assert doc.validationState == "valid"
    assert not any(i.severity == "error" for i in issues)
