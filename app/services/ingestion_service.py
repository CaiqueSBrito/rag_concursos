import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.repositories.chroma_repository import build_vectorstore_from_documents


def ingest_documents(pdf_path: str):
    """
    Le um PDF, divide em blocos e salva no banco vetorial ChromaDB.
    """
    print(f"Iniciando processamento do documento: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"Documento carregado ({len(docs)} paginas)")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    splits = text_splitter.split_documents(docs)
    print(f"Texto dividido em {len(splits)} blocos")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY,
    )

    vectorstore = build_vectorstore_from_documents(
        documents=splits,
        embeddings=embeddings,
    )

    print(
        "Banco vetorial enviado para a collection: "
        f"{settings.CHROMA_COLLECTION_NAME}"
    )
    return vectorstore


if __name__ == "__main__":
    mock_pdf = "data/raw/rag_langgraph_mock_dataset.pdf"
    if os.path.exists(mock_pdf):
        ingest_documents(mock_pdf)
    else:
        print(f"Erro: arquivo {mock_pdf} nao encontrado.")
