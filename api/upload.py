from fastapi import APIRouter, File, HTTPException, UploadFile

from models.upload import UploadResponse
from services.file_service import save_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF documents are allowed.")

    file_path = await save_file(file)

    return UploadResponse(
        filename=file_path.name,
        message="PDF uploaded successfully",
    )
