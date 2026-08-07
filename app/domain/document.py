from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentPage:
    page_number: int
    text: str

@dataclass
class Document:
    id: str
    filename: str
    path: Path
    text: str
    page_count: int


@dataclass
class ProcessedDocument:
    document: Document
