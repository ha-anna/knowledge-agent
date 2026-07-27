from fastapi import FastAPI

from app.api import chat, documents, upload
from app.core.logging import logging, setup_logging

logger = logging.getLogger(__name__)

setup_logging()

logger.info("Starting Knowledge Agent API")

app = FastAPI(
    title="Knowledge Agent API",
    version="0.1.0",
    description="An AI-powered knowledge assistant built with FastAPI and RAG.",
)

app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)

@app.get("/health")
async def health():
    return {"message": "ok"}


@app.get("/")
async def root():
    return {"name": "Knowledge Agent", "version": "0.1.0", "status": "running"}
