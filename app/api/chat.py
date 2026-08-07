import logging

from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    logger.info("Received chat request")
    
    return rag_service.answer(request.question)
