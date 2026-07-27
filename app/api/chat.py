import logging

from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(chat_request: ChatRequest) -> ChatResponse:
    logger.info("Received chat request")
    
    return {"reply": f"You said: {chat_request.message}"}
