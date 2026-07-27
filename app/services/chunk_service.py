import logging

logger = logging.getLogger(__name__)

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    logger.info(
        "Chunking text (%d characters, chunk_size=%d, overlap=%d)",
        len(text),
        chunk_size,
        overlap,
    )

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += step

    if len(chunks) > 1 and len(chunks[-1]) < chunk_size // 2:
        last = chunks.pop()
        chunks[-1] += (last)

    logger.info("Created %d chunks", len(chunks))

    for i, chunk in enumerate(chunks):
        logger.info(
            "Chunk %d (%d chars): %r",
            i + 1,
            len(chunk),
            chunk[:100],
        )

    return chunks
