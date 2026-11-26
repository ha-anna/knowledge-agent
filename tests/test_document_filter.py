from unittest.mock import Mock

from app.core.config import settings
from app.services.vector_store import VectorStore


def test_search_filters_by_document_id(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "vector_db_dir", tmp_path / "vectors")
    embedding_service = Mock()
    embedding_service.embed_text.return_value = [1.0, 0.0]
    store = VectorStore(embedding_service)

    store.collection.add(
        ids=["doc-a_1_0", "doc-b_1_0"],
        documents=["Project Alpha", "Project Beta"],
        embeddings=[[1.0, 0.0], [1.0, 0.0]],
        metadatas=[
            {"document_id": "doc-a", "filename": "a.pdf", "page_number": 1},
            {"document_id": "doc-b", "filename": "b.pdf", "page_number": 1},
        ],
    )

    unfiltered = store.search("Which projects are listed?", top_k_retrieval=2)
    assert {result.document_id for result in unfiltered} == {"doc-a", "doc-b"}

    scoped = store.search(
        "Which projects are listed?", top_k_retrieval=2, document_id="doc-a"
    )
    assert [result.chunk_id for result in scoped] == ["doc-a_1_0"]

    assert store.search("Which projects are listed?", document_id="missing") == []
    