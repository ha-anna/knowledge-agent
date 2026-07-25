from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from pathlib import Path

from services.file_service import save_file

app = FastAPI(
    title="Knowledge Agent API",
    version="0.1.0",
    description="An AI-powered knowledge assistant built with FastAPI and RAG."
)

class UploadResponse(BaseModel):
    filename: str
    message: str


@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF documents are allowed.")

    file_path = await save_file(file)

    return UploadResponse(
        filename=file_path.name,
        message="PDF uploaded successfully",
    )

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest) -> ChatResponse:
    return {"reply": f"You said: {chat_request.message}"}

@app.get("/health")
async def health():
    return {"message": "ok"}

@app.get("/")
async def root():
    return  {
            "name": "Knowledge Agent",
            "version": "0.1.0",
            "status": "running"
            }
