import logging
from pathlib import Path

from pypdf import PdfReader

from app.domain.document import Document

logger = logging.getLogger(__name__)


def extract_document(
    document_id: str,
    path: Path,
    original_filename: str,
) -> Document:
    reader = PdfReader(path)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    text = "\n".join(pages)

    return Document(
            id=document_id,
            filename=original_filename,
            path=path,
            text=text,
            page_count=len(reader.pages),
        )
    