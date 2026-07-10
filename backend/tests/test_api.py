import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_extract_en_sample_pdf(sample_en_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("sample-invoice-en.pdf", io.BytesIO(sample_en_pdf_bytes), "application/pdf")},
        data={"locale": "en"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["resultMode"] == "invoice_structured"
    assert body["data"]["invoiceNumber"] == "INV-EN-2026-0042"
    assert body["data"]["total"] == 11000.0


def test_extract_ja_sample_pdf(sample_ja_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("sample-invoice-ja.pdf", io.BytesIO(sample_ja_pdf_bytes), "application/pdf")},
        data={"locale": "ja"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["resultMode"] == "invoice_structured"
    assert body["data"]["invoiceNumber"] == "INV-JP-2026-0001"
    assert body["data"]["vendorName"] == "デモ商事株式会社"


def test_extract_generic_text_pdf_returns_preview(generic_text_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("brief.pdf", io.BytesIO(generic_text_pdf_bytes), "application/pdf")},
        data={"locale": "en"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["resultMode"] == "text_preview"
    assert body["data"] is None
    assert body["textPreview"]["characterCount"] > 0
    assert "not a supported invoice template" in body["notice"]


def test_extract_generic_text_pdf_japanese_notice(generic_text_pdf_bytes: bytes) -> None:
    response = client.post(
        "/api/v1/extract",
        files={"file": ("brief.pdf", io.BytesIO(generic_text_pdf_bytes), "application/pdf")},
        data={"locale": "ja"},
    )
    body = response.json()
    assert body["resultMode"] == "text_preview"
    assert "請求書形式" in body["notice"]


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
    assert body["resultMode"] == "invoice_structured"
    assert body["success"] is False
    assert body["data"]["validationState"] == "error"


def test_sample_pdf_download_en() -> None:
    response = client.get("/api/v1/sample-pdf?locale=en")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 100


def test_sample_pdf_download_ja() -> None:
    response = client.get("/api/v1/sample-pdf?locale=ja")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 100
