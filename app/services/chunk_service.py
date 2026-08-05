import logging

from app.domain.chunk import Chunk

logger = logging.getLogger(__name__)


def chunk_text(
    document_id: str,
    text: str,
    filename: str,
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
                id=f"{document_id}_{index}",
                document_id=document_id,
                filename=filename,
                index=index,
                text=text[start:end],
            )
        )

        start += step
        index += 1

    if len(chunks) > 1 and len(chunks[-1].text) < chunk_size // 2:
        last = chunks.pop()
        chunks[-1].text += last.text[overlap:]

    logger.info("Created %d chunks", len(chunks))

    for chunk in chunks:
        logger.info(
            "Chunk %d/%d | %d chars | %.100r",
            chunk.index + 1,
            len(chunks),
            len(chunk.text),
            chunk.text,
        )

    return chunks
