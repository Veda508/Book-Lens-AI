import re


def split_paragraphs(page_text: str) -> list[str]:
    """Split extracted page text into non-empty paragraphs."""

    normalized_text = page_text.replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n+", normalized_text)

    paragraphs = []

    for block in blocks:
        # Join line wraps within a paragraph.
        paragraph = re.sub(r"\s*\n\s*", " ", block).strip()

        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs