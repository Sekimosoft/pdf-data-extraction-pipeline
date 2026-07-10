import pdfplumber


class PdfReadError(Exception):
    pass


class PdfTextResult:
    def __init__(self, text: str, page_count: int) -> None:
        self.text = text
        self.page_count = page_count


def extract_text_from_pdf(path: str, max_pages: int) -> PdfTextResult:
    try:
        with pdfplumber.open(path) as pdf:
            if len(pdf.pages) > max_pages:
                raise PdfReadError(f"PDF exceeds {max_pages} page limit")
            parts: list[str] = []
            for page in pdf.pages[:max_pages]:
                page_text = page.extract_text() or ""
                parts.append(page_text)
            text = "\n".join(parts).strip()
            return PdfTextResult(text=text, page_count=min(len(pdf.pages), max_pages))
    except PdfReadError:
        raise
    except Exception as exc:
        raise PdfReadError("Unable to read PDF file") from exc
