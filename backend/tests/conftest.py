from pathlib import Path

import pytest

from app.fixtures.generate_fixtures import (
    generate_en_invoice,
    generate_generic_text,
    generate_incomplete_invoice,
    generate_ja_invoice,
)

FIXTURES = Path(__file__).resolve().parents[1] / "app" / "fixtures"


@pytest.fixture(scope="session", autouse=True)
def ensure_pdf_fixtures() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    if not (FIXTURES / "sample_invoice_en.pdf").exists():
        generate_en_invoice()
    if not (FIXTURES / "sample_invoice_ja.pdf").exists():
        generate_ja_invoice()
    if not (FIXTURES / "incomplete_invoice.pdf").exists():
        generate_incomplete_invoice()
    if not (FIXTURES / "generic_text.pdf").exists():
        generate_generic_text()


@pytest.fixture
def sample_en_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "sample_invoice_en.pdf").read_bytes()


@pytest.fixture
def sample_ja_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "sample_invoice_ja.pdf").read_bytes()


@pytest.fixture
def incomplete_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "incomplete_invoice.pdf").read_bytes()


@pytest.fixture
def generic_text_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "generic_text.pdf").read_bytes()
