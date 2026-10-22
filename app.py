import streamlit as st

from src.pdf_reader import extract_pages
from src.text_splitter import split_paragraphs
from src.explainer import explain_passage


st.set_page_config(
    page_title="BookLens AI",
    page_icon="📚",
    layout="wide",
)

st.title("📚 BookLens AI")
st.caption("Understand the meaning behind every page.")

uploaded_file = st.file_uploader(
    "Upload a PDF book",
    type=["pdf"],
)

if uploaded_file:
    try:
        pages = extract_pages(uploaded_file.getvalue())

        if not pages:
            st.error("No pages could be read from this PDF.")
            st.stop()

        st.success(f"Loaded {len(pages)} PDF pages.")

        page_number = st.selectbox(
            "Choose a page",
            options=list(range(1, len(pages) + 1)),
        )

        selected_page = pages[page_number - 1]
        paragraphs = split_paragraphs(selected_page["text"])

        mode = st.radio(
            "Explanation mode",
            ["Entire page", "Individual paragraph"],
            horizontal=True,
        )

        if not selected_page["text"].strip():
            st.warning(
                "This page has no extractable text. "
                "OCR support will be needed for scanned pages."
            )
            st.stop()

        if mode == "Entire page":
            passage = selected_page["text"]
            selected_label = f"Page {page_number}"

        else:
            if not paragraphs:
                st.warning("No paragraphs were detected on this page.")
                st.stop()

            paragraph_index = st.selectbox(
                "Choose a paragraph",
                options=list(range(len(paragraphs))),
                format_func=lambda i: f"Paragraph {i + 1}",
            )

            passage = paragraphs[paragraph_index]
            selected_label = (
                f"Page {page_number}, "
                f"Paragraph {paragraph_index + 1}"
            )

        st.subheader("Original text")
        st.text_area(
            selected_label,
            value=passage,
            height=220,
            disabled=True,
        )

        # Provide neighboring pages as additional context.
        start = max(0, page_number - 2)
        end = min(len(pages), page_number + 1)

        context = "\n\n".join(
            f"PDF page {p['page_number']}:\n{p['text']}"
            for p in pages[start:end]
        )

        if st.button("Explain this passage", type="primary"):
            with st.spinner("Analyzing meaning and intent..."):
                try:
                    result = explain_passage(
                        passage=passage,
                        context=context,
                        mode=mode,
                    )

                    st.subheader("Simple meaning")
                    st.write(result["simple_meaning"])

                    st.subheader("Difficult vocabulary")
                    for item in result["vocabulary"]:
                        st.markdown(
                            f"**{item['word']}** — {item['meaning']}"
                        )

                    st.subheader("Author's intent")
                    st.write(result["author_intent"])

                    st.subheader("Reasoning")
                    for point in result["reasoning"]:
                        st.markdown(f"- {point}")

                    st.subheader("Historical context")
                    st.write(result["historical_context"])

                    st.subheader("Connection to the book")
                    st.write(result["connection_to_book"])

                    st.subheader("Evidence from the passage")
                    for item in result["evidence"]:
                        st.markdown(f"> {item['quote']}")
                        st.write(item["interpretation"])

                    st.subheader("Uncertainty")
                    st.write(result["uncertainty"])

                except Exception as exc:
                    st.error(f"Explanation failed: {exc}")

    except Exception as exc:
        st.error(f"Could not process this PDF: {exc}")

        