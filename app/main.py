from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Knowledge Agent API",
    version="0.1.0",
    description="An AI-powered knowledge assistant built with FastAPI and RAG."
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
