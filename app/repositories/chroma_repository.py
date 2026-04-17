from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

from app.core.config import get_chroma_client, settings


def get_vectorstore(embeddings: Embeddings) -> Chroma:
    return Chroma(
        client=get_chroma_client(),
        collection_name=settings.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
    )


def build_vectorstore_from_documents(documents, embeddings: Embeddings) -> Chroma:
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        client=get_chroma_client(),
        collection_name=settings.CHROMA_COLLECTION_NAME,
    )
