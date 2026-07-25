from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.upload import UploadResponse
from app.services.file_service import save_file
from app.services.pdf_service import extract_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF documents are allowed.")

    document_id, file_path = await save_file(file)
    document = extract_document(
        document_id=document_id,
        pdf_path=file_path,
        original_filename=file.filename,
    )
    

    return UploadResponse(
        filename=document.filename,
        pages=document.page_count,
        characters=len(document.text),
        message="PDF uploaded successfully",
    )
