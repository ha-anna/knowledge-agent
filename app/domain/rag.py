from dataclasses import dataclass

from app.domain.search import SearchResult


@dataclass
class RAGResponse:
    answer: str
    sources: list[SearchResult]
