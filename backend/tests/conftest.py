from pathlib import Path

import pytest

from tests.fixtures.generate_fixtures import generate_incomplete_invoice, generate_sample_invoice

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session", autouse=True)
def ensure_pdf_fixtures() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    if not (FIXTURES / "sample_invoice.pdf").exists():
        generate_sample_invoice()
    if not (FIXTURES / "incomplete_invoice.pdf").exists():
        generate_incomplete_invoice()


@pytest.fixture
def sample_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "sample_invoice.pdf").read_bytes()


@pytest.fixture
def incomplete_pdf_bytes(ensure_pdf_fixtures: None) -> bytes:
    return (FIXTURES / "incomplete_invoice.pdf").read_bytes()
