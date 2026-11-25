from datetime import datetime

from pydantic import BaseModel


class DocumentMetadataResponse(BaseModel):
    id: str
    filename: str
    page_count: int
    character_count: int
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentMetadataResponse]
