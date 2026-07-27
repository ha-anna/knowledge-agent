import logging
from datetime import UTC, datetime

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.domain.document_metadata import DocumentMetadata
from app.models.upload import UploadResponse
from app.services.file_service import save_file
from app.services.metadata_service import save_metadata
from app.services.pdf_service import extract_document

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    logger.info(
        "Received upload request: %s",
        file.filename,
    )

    if file.content_type != "application/pdf":
        logger.warning(
            "Rejected upload '%s' (content type: %s)",
            file.filename,
            file.content_type,
        )
        raise HTTPException(status_code=400, detail="Only PDF documents are allowed.")

    saved_file = await save_file(file)
    document = extract_document(
        document_id=saved_file.id,
        path=saved_file.path,
        original_filename=file.filename,
    )

    metadata = DocumentMetadata(
        id=document.id,
        filename=document.filename,
        path=str(document.path),
        page_count=document.page_count,
        character_count=len(document.text),
        uploaded_at=datetime.now(UTC),
    )

    save_metadata(metadata)

    logger.info(
        "Uploaded document %s (%s)",
        saved_file.id,
        file.filename,
    )

    return UploadResponse(
        filename=document.filename,
        pages=document.page_count,
        characters=len(document.text),
        message="PDF uploaded successfully",
    )
