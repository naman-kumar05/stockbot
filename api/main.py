from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from api.agent import chat_agent
from api.memory import get_memory

app = FastAPI(title="StockBot AI", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # For future multi-user support


class ClearHistoryRequest(BaseModel):
    session_id: Optional[str] = None


@app.post("/chat")
def chat(req: ChatRequest):
    """Main chat endpoint - returns LLM-powered stock analysis."""
    return chat_agent(req.message)


@app.post("/clear-history")
def clear_history(req: ClearHistoryRequest):
    """Clear conversation history."""
    memory = get_memory()
    memory.clear_history()
    return {"status": "success", "message": "Conversation history cleared"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "StockBot AI"}
