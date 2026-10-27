from pathlib import Path
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Gemma AI Chatbot")
BASE_DIR = Path(__file__).resolve().parent

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "running", "model": "gemma2:2b"}

@app.get("/ui")
def ui():
    return FileResponse(BASE_DIR / "index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma2:2b",
            "prompt": request.message,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return {"reply": response.json()["response"]}
