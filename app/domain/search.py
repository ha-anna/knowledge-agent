from dataclasses import dataclass

from app.domain.source import Source


@dataclass
class SearchResult:
    document_id: str
    chunk_id: str
    filename: str
    page_number: int
    text: str
    distance: float

    def to_source(self) -> Source:
            return Source(
                filename=self.filename,
                page_number=self.page_number,
                chunk_id=self.chunk_id,
                distance=self.distance,
                snippet=self.text[:300],
            )