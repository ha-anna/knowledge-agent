import logging

from app.domain.chunk import Chunk
from app.domain.document import DocumentPage

logger = logging.getLogger(__name__)


def chunk_text(
    document_id: str,
    text: str,
    filename: str,
    page_number: int,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    logger.info(
        "Chunking text (%d characters, chunk_size=%d, overlap=%d)",
        len(text),
        chunk_size,
        overlap,
    )

    chunks: list[Chunk] = []

    start = 0
    step = chunk_size - overlap
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunks.append(
            Chunk(
                id=f"{document_id}_{page_number}_{index}",
                document_id=document_id,
                filename=filename,
                page_number= page_number,
                index=index,
                text=text[start:end],
            )
        )

        start += step
        index += 1

    logger.info("Created %d chunks", len(chunks))

    for chunk in chunks:
        logger.info(
            "Page %d | Chunk %d/%d | %d chars | %.100r",
            chunk.page_number,
            chunk.index + 1,
            len(chunks),
            len(chunk.text),
            chunk.text,
        )

    return chunks


def chunk_pages(
    document_id: str,
    pages: list[DocumentPage],
    filename: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[Chunk]:

    chunks = []

    for page in pages:
        page_chunks = chunk_text(
            document_id=document_id,
            text=page.text,
            filename=filename,
            page_number=page.page_number,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        chunks.extend(page_chunks)

    return chunks
