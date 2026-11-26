from unittest.mock import Mock
import pytest

from fastapi.testclient import TestClient

from app.core.dependencies.rag import get_rag_service
from app.domain.rag import RAGResponse
from app.main import app


def test_message_forwards_document_id(monkeypatch):
    rag = Mock()
    rag.answer.return_value = RAGResponse(answer="VisionX", sources=[])
    monkeypatch.setitem(app.dependency_overrides, get_rag_service, lambda: rag)

    with TestClient(app) as client:
        created = client.post("/conversations/")
        assert created.status_code in (200, 201)
        conversation_id = created.json()["id"]

        response = client.post(
            f"/conversations/{conversation_id}/messages",
            json={
                "content": "Which projects are listed?",
                "document_id": "test-document",
            },
        )

    assert response.status_code == 200
    rag.answer.assert_called_once_with(
        "Which projects are listed?",
        [],
        document_id="test-document",
    )
    assert response.json()["messages"][-1]["content"] == "VisionX"


@pytest.mark.parametrize("content", ["", "   "])
def test_message_rejects_blank_content(monkeypatch, content):
    rag = Mock()
    monkeypatch.setitem(app.dependency_overrides, get_rag_service, lambda: rag)

    with TestClient(app) as client:
        created = client.post("/conversations/")
        assert created.status_code in (200, 201)
        conversation_id = created.json()["id"]

        response = client.post(
            f"/conversations/{conversation_id}/messages",
            json={"content": content},
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "content"]
    rag.answer.assert_not_called()


def test_failed_generation_leaves_history_unchanged(monkeypatch):
    rag = Mock()
    rag.answer.side_effect = [
        RuntimeError("simulated generation failure"),
        RAGResponse(answer="The retry worked.", sources=[]),
    ]
    monkeypatch.setitem(app.dependency_overrides, get_rag_service, lambda: rag)

    with TestClient(app, raise_server_exceptions=False) as client:
        created = client.post("/conversations/")
        assert created.status_code in (200, 201)
        conversation_id = created.json()["id"]
        url = f"/conversations/{conversation_id}/messages"

        failed = client.post(url, json={"content": "First attempt"})
        assert failed.status_code == 500

        retried = client.post(url, json={"content": "Second attempt"})
        assert retried.status_code == 200

    rag.answer.assert_called_with("Second attempt", [], document_id=None)
    assert [
        (message["role"], message["content"])
        for message in retried.json()["messages"]
    ] == [
        ("user", "Second attempt"),
        ("assistant", "The retry worked."),
    ]
