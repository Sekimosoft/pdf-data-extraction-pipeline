from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent


def sample_invoice_path(locale: str = "en") -> Path:
    name = "sample_invoice_ja.pdf" if locale == "ja" else "sample_invoice_en.pdf"
    return FIXTURES_DIR / name
