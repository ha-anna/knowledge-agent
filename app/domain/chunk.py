from dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    document_id: str
    index: int
    text: str


@dataclass
class EmbeddedChunk:
    chunk: Chunk
    embedding: list[float]

