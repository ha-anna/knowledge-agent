from fastapi import FastAPI

from app.api import chat, upload

app = FastAPI(
    title="Knowledge Agent API",
    version="0.1.0",
    description="An AI-powered knowledge assistant built with FastAPI and RAG.",
)

app.include_router(chat.router)
app.include_router(upload.router)


@app.get("/health")
async def health():
    return {"message": "ok"}


@app.get("/")
async def root():
    return {"name": "Knowledge Agent", "version": "0.1.0", "status": "running"}
