from dataclasses import asdict, dataclass
from datetime import datetime

from app.models.document import DocumentMetadataResponse


@dataclass
class DocumentMetadata:
    id: str
    filename: str
    path: str
    page_count: int
    character_count: int
    uploaded_at: datetime

    def to_dict(self) -> dict:
        data = asdict(self)
        data["uploaded_at"] = self.uploaded_at.isoformat()
        return data

    def to_response(self) -> DocumentMetadataResponse:
        return DocumentMetadataResponse(
            id=self.id,
            filename=self.filename,
            page_count=self.page_count,
            character_count=self.character_count,
            uploaded_at=self.uploaded_at,
        )
    
    @classmethod
    def from_dict(cls, data: dict) -> "DocumentMetadata":
        return cls(
            id=data["id"],
            filename=data["filename"],
            path=data["path"],
            page_count=data["page_count"],
            character_count=data["character_count"],
            uploaded_at=datetime.fromisoformat(data["uploaded_at"]),
        )