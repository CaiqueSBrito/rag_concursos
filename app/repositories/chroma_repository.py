import chromadb
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from fastapi import Depends
from app.core.config import get_chroma_client, settings

_client: ClientAPI | None = None
_collection: Collection | None = None

def get_chroma_client() -> ClientAPI:
	global _client
	if _client is None:
		_client = chromadb.CloudClient(
            api_key=settings.CHROMA_API_KEY,
            tenant=settings.CHROMA_TENANT,
            database=settings.CHROMA_DATABASE
        )
	return _client

def get_chroma_collection(client: ClientAPI = Depends(get_chroma_client)) -> Collection:
	global _collection
	if _collection is None:
		_collection = client.get_or_create_collection(
		    name=settings.CHROMA_COLLECTION_NAME,
		)
	return _collection

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
