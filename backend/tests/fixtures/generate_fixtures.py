"""Generate synthetic invoice PDF fixtures — fictional data only, no external deps."""

from pathlib import Path


FIXTURES_DIR = Path(__file__).resolve().parent
SAMPLE_INVOICE = FIXTURES_DIR / "sample_invoice.pdf"
INCOMPLETE_INVOICE = FIXTURES_DIR / "incomplete_invoice.pdf"


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_text_pdf(lines: list[str]) -> bytes:
    """Minimal text-only PDF (Type 1 font Helvetica)."""
    y = 750
    content_parts: list[str] = ["BT /F1 12 Tf"]
    for line in lines:
        content_parts.append(f"1 0 0 1 72 {y} Tm ({_escape_pdf_text(line)}) Tj")
        y -= 18
    content_parts.append("ET")
    stream = "\n".join(content_parts).encode("latin-1")

    objects: list[bytes] = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
    )
    objects.append(
        f"4 0 obj << /Length {len(stream)} >> stream\n".encode("ascii")
        + stream
        + b"\nendstream endobj\n"
    )
    objects.append(
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode(
            "ascii"
        )
    )
    return bytes(pdf)


def generate_sample_invoice() -> None:
    lines = [
        "INVOICE",
        "Document Type: invoice",
        "Invoice Number: INV-2026-0042",
        "Issue Date: 2026-03-15",
        "Due Date: 2026-04-15",
        "Vendor: Acme Supplies Co.",
        "Customer: Demo Retail Ltd.",
        "Subtotal: 10000.00",
        "Tax: 1000.00",
        "Total: 11000.00",
        "Currency: JPY",
    ]
    SAMPLE_INVOICE.write_bytes(build_text_pdf(lines))


def generate_incomplete_invoice() -> None:
    lines = [
        "INVOICE",
        "Document Type: invoice",
        "Vendor: Partial Data Inc.",
        "Customer: Test Buyer",
    ]
    INCOMPLETE_INVOICE.write_bytes(build_text_pdf(lines))


if __name__ == "__main__":
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    generate_sample_invoice()
    generate_incomplete_invoice()
    print(f"Wrote {SAMPLE_INVOICE.name} and {INCOMPLETE_INVOICE.name}")
