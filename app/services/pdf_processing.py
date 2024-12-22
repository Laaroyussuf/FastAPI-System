import os
from PyPDF2 import PdfReader

def split_pdf_into_pages(pdf_path: str) -> list:
    """
    Split a PDF file into pages and extract text content.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: A list of dictionaries containing page number and content.
    """
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        pages.append({"page_number": i + 1, "content": text})
    return pages
