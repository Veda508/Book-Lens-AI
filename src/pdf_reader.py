import fitz  # PyMuPDF


def extract_pages(pdf_bytes: bytes) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    pages = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            pages.append({
                "page_number": page_number,
                "text": text,
            })

    return pages