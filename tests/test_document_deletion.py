import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.core.config import settings
from app.domain.document_metadata import DocumentMetadata
from app.services import document_service
from app.services.metadata_service import save_metadata
from app.services.vector_store import VectorStore


def test_delete_document_removes_pdf_metadata_and_vectors(tmp_path, monkeypatch):
    for name in ("upload_dir", "metadata_dir", "vector_db_dir"):
        directory = tmp_path / name
        directory.mkdir()
        monkeypatch.setattr(settings, name, directory)

    embedding = Mock()
    embedding.embed_text.return_value = [1.0, 0.0]
    store = VectorStore(embedding)
    monkeypatch.setattr(document_service, "vector_store", store)

    document_id = "test-doc"
    pdf_path = settings.upload_dir / f"{document_id}.pdf"
    pdf_path.touch()
    save_metadata(
        DocumentMetadata(
            id=document_id,
            filename="test.pdf",
            path=str(pdf_path),
            page_count=1,
            character_count=13,
            uploaded_at=datetime.now(UTC),
        )
    )
    store.collection.add(
        ids=["test-doc_1_0"],
        documents=["Project Alpha"],
        embeddings=[[1.0, 0.0]],
        metadatas=[
            {"document_id": document_id, "filename": "test.pdf", "page_number": 1}
        ],
    )
    assert store.search("Project Alpha", document_id=document_id)

    document_service.delete_document(document_id)

    assert not pdf_path.exists()
    assert not (settings.metadata_dir / f"{document_id}.json").exists()
    assert store.search("Project Alpha", document_id=document_id) == []


def test_failed_upload_rolls_back_partial_writes(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "metadata_dir", tmp_path)
    pdf_path = tmp_path / "test-doc.pdf"
    pdf_path.touch()

    async def fake_save_file(file):
        return SimpleNamespace(id="test-doc", path=pdf_path)

    def save_then_fail(metadata):
        save_metadata(metadata)
        raise OSError("simulated metadata write failure")

    store = Mock()
    monkeypatch.setattr(document_service, "vector_store", store)
    monkeypatch.setattr(document_service, "embedding_service", Mock())
    monkeypatch.setattr(document_service, "save_file", fake_save_file)
    monkeypatch.setattr(document_service, "chunk_pages", Mock())
    monkeypatch.setattr(document_service, "save_metadata", save_then_fail)
    monkeypatch.setattr(
        document_service,
        "extract_document",
        Mock(return_value=SimpleNamespace(
            id="test-doc",
            filename="test.pdf",
            path=pdf_path,
            text="Project Alpha",
            pages=[],
            page_count=1,
        )),
    )

    with pytest.raises(OSError, match="simulated metadata write failure"):
        asyncio.run(
            document_service.process_document(SimpleNamespace(filename="test.pdf"))
        )

    store.add.assert_called_once()
    store.delete_document.assert_called_once_with("test-doc")
    assert not pdf_path.exists()
    assert not (tmp_path / "test-doc.json").exists()
