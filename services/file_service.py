from pathlib import Path
from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_file(file: UploadFile) -> Path:
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    await file.close()

    return file_path
