from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    pages: int
    characters: int
    message: str
