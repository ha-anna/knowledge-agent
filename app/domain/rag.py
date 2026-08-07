from dataclasses import dataclass

from app.domain.source import Source


@dataclass
class RAGResponse:
    answer: str
    sources: list[Source]
