import pdfplumber


class PdfReadError(Exception):
    pass


def extract_text_from_pdf(path: str, max_pages: int) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            if len(pdf.pages) > max_pages:
                raise PdfReadError(f"PDF exceeds {max_pages} page limit")
            parts: list[str] = []
            for page in pdf.pages[:max_pages]:
                page_text = page.extract_text() or ""
                parts.append(page_text)
            return "\n".join(parts).strip()
    except PdfReadError:
        raise
    except Exception as exc:
        raise PdfReadError("Unable to read PDF file") from exc
