from dataclasses import dataclass


@dataclass
class SearchResult:
    document_id: str
    chunk_id: str
    text: str
    score: float
