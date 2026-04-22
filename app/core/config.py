from typing import Literal

import chromadb
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangGraph RAG"

    EMBEDDING_PROVIDER: Literal["google", "huggingface"] = "huggingface"

    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"
    GEMINI_EMBEDDING_DIMENSIONS: int = 768

    HUGGINGFACE_EMBEDDING_MODEL: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    HUGGINGFACE_EMBEDDING_DEVICE: str = "cpu"
    HUGGINGFACE_NORMALIZE_EMBEDDINGS: bool = True
    
    CHROMA_API_KEY: str = Field(
        ...,
        validation_alias=AliasChoices("CHROMA_API_KEY", "CHROMA_DB_KEY"),
    )
    CHROMA_TENANT: str = Field(
        ...,
        validation_alias=AliasChoices("CHROMA_TENANT", "TENANT"),
    )
    CHROMA_DATABASE: str = Field(
        ...,
        validation_alias=AliasChoices("CHROMA_DATABASE", "DATABASE"),
    )
    CHROMA_COLLECTION_NAME: str = Field(
        default="rag_documents",
        validation_alias=AliasChoices("CHROMA_COLLECTION_NAME"),
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def get_chroma_client() -> chromadb.ClientAPI:
    return chromadb.CloudClient(
        api_key=settings.CHROMA_API_KEY,
        tenant=settings.CHROMA_TENANT,
        database=settings.CHROMA_DATABASE,
    )
