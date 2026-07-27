import logging

from app.services.file_service import delete_file
from app.services.metadata_service import delete_metadata

logger = logging.getLogger(__name__)


def delete_document(document_id: str) -> None:
    delete_file(document_id)
    delete_metadata(document_id)
