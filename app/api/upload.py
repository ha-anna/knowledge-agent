import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.upload import UploadResponse
from app.services.document_service import process_document

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    logger.info("Received upload request: %s", file.filename)

    if file.content_type != "application/pdf":
        logger.warning(
            "Rejected upload '%s' (content type: %s)",
            file.filename,
            file.content_type,
        )
        raise HTTPException(
            status_code=400,
            detail="Only PDF documents are allowed.",
        )

    processed = await process_document(file)

    logger.info(
        "Uploaded document %s (%s)",
        processed.document.id,
        processed.document.filename,
    )

    return UploadResponse(
        filename=processed.document.filename,
        pages=processed.document.page_count,
        characters=len(processed.document.text),
        message="PDF uploaded successfully",
    )