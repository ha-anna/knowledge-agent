import json
import logging

from app.core.config import settings
from app.domain.document_metadata import DocumentMetadata

logger = logging.getLogger(__name__)

settings.metadata_dir.mkdir(parents=True, exist_ok=True)


def save_metadata(metadata: DocumentMetadata) -> None:
    metadata_path = settings.metadata_dir / f"{metadata.id}.json"

    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(
            metadata.to_dict(),
            f,
            indent=4,
        )

def load_metadata(document_id: str) -> DocumentMetadata:
    metadata_path = settings.metadata_dir / f"{document_id}.json"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Document '{document_id}' not found."
        )

    with metadata_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return DocumentMetadata.from_dict(data)

def list_metadata() -> list[DocumentMetadata]:
    documents = []

    for metadata_file in settings.metadata_dir.glob("*.json"):
        with metadata_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        documents.append(DocumentMetadata.from_dict(data))

    return documents

def delete_metadata(document_id: str) -> None:
    metadata_path = settings.metadata_dir / f"{document_id}.json"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata for document '{document_id}' not found."
        )

    metadata_path.unlink()
