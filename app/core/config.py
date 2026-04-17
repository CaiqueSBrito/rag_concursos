import chromadb
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangGraph RAG"
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
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
