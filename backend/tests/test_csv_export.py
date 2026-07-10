import csv
import io

from app.models.schemas import ExtractedDocument


def document_to_csv_row(doc: ExtractedDocument) -> dict[str, str]:
    return {
        "documentType": doc.documentType or "",
        "invoiceNumber": doc.invoiceNumber or "",
        "issueDate": doc.issueDate or "",
        "dueDate": doc.dueDate or "",
        "vendorName": doc.vendorName or "",
        "customerName": doc.customerName or "",
        "subtotal": "" if doc.subtotal is None else str(doc.subtotal),
        "tax": "" if doc.tax is None else str(doc.tax),
        "total": "" if doc.total is None else str(doc.total),
        "currency": doc.currency or "",
        "confidence": str(doc.confidence),
        "validationState": doc.validationState,
    }


def export_csv(doc: ExtractedDocument) -> str:
    row = document_to_csv_row(doc)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)
    return buffer.getvalue()


def test_csv_export_columns() -> None:
    doc = ExtractedDocument(
        documentType="invoice",
        invoiceNumber="INV-1",
        issueDate="2026-01-01",
        dueDate="2026-02-01",
        vendorName="V",
        customerName="C",
        subtotal=100.0,
        tax=10.0,
        total=110.0,
        currency="JPY",
        confidence=0.9,
        validationState="valid",
    )
    csv_text = export_csv(doc)
    assert "invoiceNumber" in csv_text
    assert "INV-1" in csv_text
    assert "validationState" in csv_text
