from pydantic_settings import BaseSettings, SettingsConfigDict
import chromadb
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangGraph RAG"
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    VECTORSTORE_PATH: str = "data/vectorstore"
    CHROMA_DB_KEY: str = Field(..., env="CHROMA_DB_KEY")
    TENANT: str = Field(..., env="TENANT")
    DATABASE: str = Field(..., env="DATABASE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

client = chromadb.CloudClient(
    api_key = settings.CHROMA_DB_KEY,
    tenant = settings.TENANT,
    database = settings.DATABASE
)