from app.extraction.invoice_parser import parse_invoice_text
from app.validation.rules import validate_extraction


def test_parse_invoice_text_full() -> None:
    text = """
    INVOICE
    Document Type: invoice
    Invoice Number: INV-2026-0042
    Issue Date: 2026-03-15
    Due Date: 2026-04-15
    Vendor: Acme Supplies Co.
    Customer: Demo Retail Ltd.
    Subtotal: 10,000.00
    Tax: 1,000.00
    Total: 11,000.00
    Currency: JPY
    """
    parsed = parse_invoice_text(text)
    assert parsed["invoiceNumber"] == "INV-2026-0042"
    assert parsed["total"] == 11000.0
    assert parsed["currency"] == "JPY"


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
    assert doc.confidence >= 0.8
    assert not any(i.severity == "error" for i in issues)


def test_validation_total_mismatch_warning() -> None:
    parsed = {
        "documentType": "invoice",
        "invoiceNumber": "INV-2",
        "issueDate": "2026-01-01",
        "dueDate": "2026-02-01",
        "subtotal": 100.0,
        "tax": 10.0,
        "total": 999.0,
        "currency": "USD",
    }
    doc, issues = validate_extraction(parsed, "en")
    assert doc.validationState == "warning"
    assert any("match" in i.message.lower() for i in issues)
