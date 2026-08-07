from dataclasses import dataclass


@dataclass
class Source:
    filename: str
    page_number: int
    chunk_id: str
    distance: float
    snippet: str
