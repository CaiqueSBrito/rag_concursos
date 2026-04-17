from fastapi import FastAPI
from app.api.endpoints.chat import router as chat_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo a API RAG com LangGraph e Gemini!"}
