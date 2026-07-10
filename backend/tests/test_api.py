import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_extract_valid_sample_pdf(sample_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("sample-invoice.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
        data={"locale": "en"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["invoiceNumber"] == "INV-2026-0042"
    assert body["data"]["total"] == 11000.0
    assert body["data"]["validationState"] in {"valid", "warning"}


def test_extract_japanese_locale_messages(sample_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("sample-invoice.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
        data={"locale": "ja"},
    )
    assert response.status_code == 200
    assert response.json()["locale"] == "ja"


def test_unsupported_file_type() -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")},
        data={"locale": "en"},
    )
    assert response.status_code == 400


def test_oversized_file() -> None:
    big = b"%PDF-" + b"0" * (6 * 1024 * 1024)
    response = client.post(
        "/api/v1/extract",
        files={"file": ("big.pdf", io.BytesIO(big), "application/pdf")},
        data={"locale": "en"},
    )
    assert response.status_code == 400


def test_incomplete_invoice_validation(incomplete_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("incomplete.pdf", io.BytesIO(incomplete_pdf_bytes), "application/pdf")},
        data={"locale": "en"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["data"]["validationState"] == "error"
    assert len(body["validationIssues"]) >= 1


def test_sample_pdf_download() -> None:
    response = client.get("/api/v1/sample-pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 100
