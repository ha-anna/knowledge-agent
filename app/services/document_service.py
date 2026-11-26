import logging
from datetime import UTC, datetime

from fastapi import UploadFile

from app.core.config import settings
from app.core.dependencies.embedding import embedding_service
from app.core.dependencies.vector_store import vector_store
from app.domain.document import ProcessedDocument
from app.domain.document_metadata import DocumentMetadata
from app.services.chunk_service import chunk_pages
from app.services.file_service import delete_file, save_file
from app.services.metadata_service import delete_metadata, load_metadata, save_metadata
from app.services.pdf_service import extract_document


logger = logging.getLogger(__name__)


class NoExtractableTextError(ValueError):
    pass


async def process_document(file: UploadFile) -> ProcessedDocument:
    indexing_started = False
    metadata_write_started = False
    saved_file = await save_file(file)

    try:
        document = extract_document(
            document_id=saved_file.id,
            path=saved_file.path,
            original_filename=file.filename,
        )

        if not document.text.strip():
            raise NoExtractableTextError("This PDF has no extractable text.")

        chunks = chunk_pages(
            document_id=document.id,
            pages=document.pages,
            filename=document.filename,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )

        embedded_chunks = embedding_service.embed_chunks(chunks)

        indexing_started = True
        vector_store.add(embedded_chunks)

        metadata = DocumentMetadata(
            id=document.id,
            filename=document.filename,
            path=str(document.path),
            page_count=document.page_count,
            character_count=len(document.text),
            uploaded_at=datetime.now(UTC),
        )

        metadata_write_started = True
        save_metadata(metadata)

        return ProcessedDocument(
            document=document,
        )
    except Exception:
        if metadata_write_started:
            try:
                delete_metadata(saved_file.id)
            except FileNotFoundError:
                pass
            except Exception:
                logger.exception("Could not clean up metadata for %s", saved_file.id)

        if indexing_started:
            try:
                vector_store.delete_document(saved_file.id)
            except Exception:
                logger.exception("Could not clean up vectors for %s", saved_file.id)

        try:
            saved_file.path.unlink(missing_ok=True)
        except OSError:
            logger.exception("Could not clean up PDF for %s", saved_file.id)

        raise


def delete_document(document_id: str) -> None:
    load_metadata(document_id)
    vector_store.delete_document(document_id)

    try:
        delete_file(document_id)
    except FileNotFoundError:
        pass

    delete_metadata(document_id)
