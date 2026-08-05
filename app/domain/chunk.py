from dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    document_id: str
    filename: str
    index: int
    text: str


@dataclass
class EmbeddedChunk:
    source_chunk: Chunk
    embedding: list[float]

