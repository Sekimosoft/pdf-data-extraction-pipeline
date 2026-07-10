"""Generate synthetic PDF fixtures — fictional data only."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

FIXTURES_DIR = Path(__file__).resolve().parent
FONT = "HeiseiKakuGo-W5"


def _draw_lines(path: Path, lines: list[str], use_unicode: bool = False) -> None:
    pdfmetrics.registerFont(UnicodeCIDFont(FONT))
    c = canvas.Canvas(str(path), pagesize=letter)
    font = FONT if use_unicode else "Helvetica"
    y = 750
    for line in lines:
        c.setFont(font, 12)
        c.drawString(72, y, line)
        y -= 22
    c.save()


def generate_en_invoice() -> None:
    lines = [
        "INVOICE",
        "Document Type: invoice",
        "Invoice Number: INV-EN-2026-0042",
        "Issue Date: 2026-03-15",
        "Due Date: 2026-04-15",
        "Vendor: Acme Supplies Co.",
        "Customer: Demo Retail Ltd.",
        "Subtotal: 10000.00",
        "Tax: 1000.00",
        "Total: 11000.00",
        "Currency: USD",
    ]
    _draw_lines(FIXTURES_DIR / "sample_invoice_en.pdf", lines)


def generate_ja_invoice() -> None:
    lines = [
        "請求書",
        "書類種別: invoice",
        "請求書番号: INV-JP-2026-0001",
        "発行日: 2026-03-15",
        "支払期限: 2026-04-15",
        "発行元: デモ商事株式会社",
        "請求先: サンプル小売店",
        "小計: 10000.00",
        "消費税: 1000.00",
        "合計: 11000.00",
        "通貨: JPY",
    ]
    _draw_lines(FIXTURES_DIR / "sample_invoice_ja.pdf", lines, use_unicode=True)


def generate_incomplete_invoice() -> None:
    lines = [
        "INVOICE",
        "Document Type: invoice",
        "Vendor: Partial Data Inc.",
        "Customer: Test Buyer",
    ]
    _draw_lines(FIXTURES_DIR / "incomplete_invoice.pdf", lines)


def generate_generic_text() -> None:
    lines = [
        "Project Brief: BI Platform Consultation",
        "This document outlines a fictional RFI for a demo data warehouse project.",
        "It is not an invoice and should return text preview only.",
        "Contact: demo-analyst@example.invalid",
    ]
    _draw_lines(FIXTURES_DIR / "generic_text.pdf", lines)


if __name__ == "__main__":
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    generate_en_invoice()
    generate_ja_invoice()
    generate_incomplete_invoice()
    generate_generic_text()
    print("Wrote sample_invoice_en.pdf, sample_invoice_ja.pdf, incomplete_invoice.pdf, generic_text.pdf")
