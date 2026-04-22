import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.repositories.chroma_repository import build_vectorstore_from_documents
from app.services.embedding_service import get_embeddings_model


def ingest_documents(pdf_path: str):
    """
    Le um PDF, divide em blocos e salva no banco vetorial ChromaDB.
    """
    print(f"Iniciando processamento do documento: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"Documento carregado ({len(docs)} paginas)")

    text_chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_chunks.split_documents(docs)
    for index, chunk in enumerate(chunks):
        page = chunk.metadata.get("page", "na")
        chunk.metadata["chunk_id"] = f"{pdf_path}:{page}:{index}"
    print(f"Texto dividido em {len(chunks)} blocos")

    embeddings = get_embeddings_model()

    vectorstore = build_vectorstore_from_documents(
        documents=chunks,
        embeddings=embeddings,
    )

    print(
        "Banco vetorial enviado para a collection: "
        f"{settings.CHROMA_COLLECTION_NAME}"
    )
    return vectorstore


if __name__ == "__main__":
    mock_pdf = "data/raw/rag_langgraph_mock_da4taset.pdf"
    if os.path.exists(mock_pdf):
        ingest_documents(mock_pdf)
    else:
        print(f"Erro: arquivo {mock_pdf} nao encontrado.")
