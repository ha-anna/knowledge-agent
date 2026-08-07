import logging
from datetime import UTC, datetime

from fastapi import UploadFile

from app.core.dependencies.embedding import embedding_service
from app.core.dependencies.vector_store import vector_store
from app.domain.document import ProcessedDocument
from app.domain.document_metadata import DocumentMetadata
from app.services.chunk_service import chunk_pages
from app.services.file_service import delete_file, save_file
from app.services.metadata_service import delete_metadata, save_metadata
from app.services.pdf_service import extract_document

logger = logging.getLogger(__name__)

async def process_document(file: UploadFile) -> ProcessedDocument:
    saved_file = await save_file(file)

    document = extract_document(
        document_id=saved_file.id,
        path=saved_file.path,
        original_filename=file.filename,
    )

    chunks = chunk_pages(
        document_id=document.id,
        pages=document.pages,
        filename=document.filename,
    )


    embedded_chunks = embedding_service.embed_chunks(chunks)

    logger.info(
        "Embedding dimension: %d",
        len(embedded_chunks[0].embedding),
    )

    vector_store.add(embedded_chunks)

    metadata = DocumentMetadata(
        id=document.id,
        filename=document.filename,
        path=str(document.path),
        page_count=document.page_count,
        character_count=len(document.text),
        uploaded_at=datetime.now(UTC),
    )

    save_metadata(metadata)

    return ProcessedDocument(
        document=document,
    )


def delete_document(document_id: str) -> None:
    delete_file(document_id)
    delete_metadata(document_id)
