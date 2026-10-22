import fitz

from src.pdf_reader import extract_pages


def test_extract_pages():
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "A book about political philosophy.")

    pdf_bytes = document.tobytes()
    document.close()

    pages = extract_pages(pdf_bytes)

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "political philosophy" in pages[0]["text"]