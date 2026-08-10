import logging

from fastapi import APIRouter, Depends

from app.core.dependencies.conversation_store import get_conversation_store
from app.core.dependencies.rag import get_rag_service
from app.domain.conversation import Message
from app.models.chat import MessageRequest
from app.services.conversation_store import ConversationStore
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/")
def create_conversation(
    conversation_store: ConversationStore = Depends(get_conversation_store),
):
    conversation = conversation_store.create()

    return conversation


@router.post("/{conversation_id}/messages")
def send_message(
    conversation_id: str,
    request: MessageRequest,
    conversation_store: ConversationStore = Depends(get_conversation_store),
    rag_service: RAGService = Depends(get_rag_service),
):
    user_message = Message(
        role="user",
        content=request.content,
    )

    conversation_store.add_message(
        conversation_id,
        user_message,
    )

    conversation = conversation_store.get(conversation_id)

    history = conversation.messages[:-1]

    rag_response = rag_service.answer(
        request.content,
        history,
    )

    assistant_message = Message(
        role="assistant",
        content=rag_response.answer,
    )

    conversation_store.add_message(
        conversation_id,
        assistant_message,
    )

    return conversation_store.get(conversation_id)
