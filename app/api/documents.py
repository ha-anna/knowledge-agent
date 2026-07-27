import logging

from fastapi import APIRouter, HTTPException

from app.models.document import DocumentListResponse, DocumentMetadataResponse
from app.services.document_service import delete_document
from app.services.metadata_service import list_metadata, load_metadata

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get("", response_model=DocumentListResponse)
async def list_documents() -> DocumentListResponse:
    logger.info("Listing all documents")
    documents = list_metadata()

    logger.info(
        "Returned %d documents",
        len(documents),
    )
    return DocumentListResponse(
        documents=[doc.to_response() for doc in documents]
    )


@router.get(
    "/{document_id}",
    response_model=DocumentMetadataResponse,
)
async def get_document(document_id: str) -> DocumentMetadataResponse:
    try:
        logger.info(
            "Fetching document %s",
            document_id,
        )

        metadata = load_metadata(document_id)
    except FileNotFoundError as e:
        logger.warning(str(e))

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return metadata.to_response()

@router.delete("/{document_id}", status_code=204)
async def delete_document_endpoint(document_id: str):
    try:
        logger.info(
            "Deleting document %s",
            document_id,
        )

        delete_document(document_id)

        logger.info(
            "Deleted document %s",
            document_id,
        )
    except FileNotFoundError as e:
        logger.warning(str(e))
        
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )