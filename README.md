# PDF Data Extraction Pipeline

**Turn text-based PDF invoices into validated structured data — JSON or CSV — in one step.**

Upload a PDF → extract fields → validate → copy JSON or download CSV. Built as portfolio evidence for document ingestion workflows, not as a universal AI PDF parser.

---

## Business problem

Finance and operations teams receive PDF invoices and forms, then manually re-type amounts, dates, and vendor details into spreadsheets or ERP systems. That work is slow, error-prone, and hard to audit.

This demo proves a focused pipeline: **PDF in → validated structured records out**, with deterministic rules you can test and explain to a buyer.

---

## Live demo

**Status:** Not deployed yet — Live Demo pending one-time [Render](https://render.com) GitHub OAuth (same as Project 01).

**Run locally:** see [How to run](#how-to-run) below. Use the included **sample PDF** — do not upload real customer documents.

---

## Screenshots

| English | Japanese |
|---|---|
| ![Upload EN](docs/screenshots/screenshot-en.png) | ![Upload JA](docs/screenshots/screenshot-ja.png) |

---

## How it works

```text
Upload PDF → Text extract (pdfplumber) → Rule-based field parse → Validation → JSON / CSV
```

1. User uploads a **text-based PDF** (single-page invoice template in V1).
2. Backend extracts raw text with **pdfplumber** — no OCR, no AI API.
3. **Deterministic regex parsers** map labels to schema fields.
4. **Validation rules** check required fields, dates, amounts, and totals.
5. UI shows structured result with validation state; user copies JSON or downloads CSV.

---

## Supported document scope (V1)

| Supported | Not supported in V1 |
|---|---|
| Text-based PDF (selectable text) | Scanned / image-only PDFs |
| Single synthetic invoice template | Arbitrary document layouts |
| English label patterns in sample (`Invoice Number:`, `Total:`, etc.) | OCR |
| Up to 5 MB, 10 pages | Password-protected PDFs |
| Fictional demo PDF only | Real customer documents |

**Honest scope:** V1 is **not** a “read any PDF with AI” product. It demonstrates **document parsing + schema validation** for one invoice pattern.

---

## Architecture

```text
┌─────────────┐     multipart      ┌──────────────────┐
│  Next.js    │ ────────────────►  │  FastAPI         │
│  Upload UI  │ ◄────────────────  │  Extract API     │
└─────────────┘     JSON           └────────┬─────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    ▼                       ▼                       ▼
              pdfplumber              invoice_parser           validation
              (text extract)          (regex rules)            (Pydantic)
```

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, React 19 |
| Backend | FastAPI, Python 3.12, Pydantic v2 |
| PDF | pdfplumber |
| Storage | None — in-memory processing only |
| Database | None |
| AI | None in V1 |

**Different from [AI Lead Triage CRM Router](https://github.com/Sekimosoft/ai-lead-triage-crm-router):** Project 01 interprets **free-text inquiries** with AI. Project 02 parses **binary PDF documents** with deterministic extraction — different buyer pain, different proof.

---

## Design principles

- Prove **document ingestion**, not conversational AI.
- **Deterministic validation** before export — fail safely on bad data.
- **No persistence** of uploaded files.
- **Minimal V1 scope** — one template, honest README boundaries.
- EN / JP UI for Japan invoice workflow context; JSON field names stay English.

---

## Key design decisions

| Decision | Why |
|---|---|
| **Text-based PDF only in V1** | Many business PDFs are text-native; OCR adds cost and changes the proof focus. |
| **No OCR** | Keeps V1 small, testable, and honest — scanned docs get a clear error. |
| **Deterministic extraction before AI** | Business-critical fields should be validated by rules, not guessed. |
| **Files not persisted** | Demo privacy and simpler deployment — no storage liability. |
| **Validation separated from extraction** | Parsing can succeed partially; validation flags what is safe to export. |

---

## Security and privacy

- **Demo only** — do not upload real customer documents.
- **No persistent storage** — PDFs processed in memory and discarded.
- MIME type and `.pdf` extension checks; max **5 MB** file size.
- Filename is not trusted for security decisions.
- Temp files deleted after processing.
- No secrets in repository — use `.env.example` only.

---

## How to run

### Prerequisites

- Python 3.12+
- Node.js 22+

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Open http://localhost:3000 — download the sample PDF, upload it, extract.

### Docker (optional)

```bash
docker compose up --build
```

---

## Testing

```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm test && npm run lint && npm run build
```

GitHub Actions runs both on push to `main`.

---

## Copyright

Copyright © Sekimosoft. No license is granted for reuse.

---

**Sekimosoft** · Portfolio project · Related: [BizDXAI](https://github.com/Sekimosoft) product work remains private; this repo is independent public evidence.
