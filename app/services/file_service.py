
import uuid

from fastapi import UploadFile

from app.core.config import settings
from app.models.saved_file import SavedFile

settings.upload_dir.mkdir(exist_ok=True)


async def save_file(file: UploadFile) -> SavedFile:
    document_id = str(uuid.uuid4())
    file_path = settings.upload_dir / f"{document_id}.pdf"

    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    await file.close()

    return SavedFile(
        id=document_id,
        path=file_path,
    )
