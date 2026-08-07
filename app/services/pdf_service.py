import logging
from pathlib import Path

from pypdf import PdfReader

from app.domain.document import Document, DocumentPage

logger = logging.getLogger(__name__)


def extract_document(
    document_id: str,
    path: Path,
    original_filename: str,
) -> Document:
    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            pages.append(
                DocumentPage(
                    page_number=page_number,
                    text=page_text,
                )
            )

    text = "\n".join(
        page.text for page in pages
    )

    return Document(
        id=document_id,
        filename=original_filename,
        path=path,
        text=text,
        pages=pages,
        page_count=len(reader.pages),
    )
    