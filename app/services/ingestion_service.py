from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
import os

def ingest_documents(pdf_path: str):
    """
    Lê um PDF, divide em blocos e salva no banco vetorial ChromaDB.
    """
    print(f"📄 Iniciando processamento do documento: {pdf_path}")
    
    # 1. Carregamento
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"✅ Documento carregado ({len(docs)} páginas)")

    # 2. Divisão (Chunking)
    # Usamos 1000 caracteres com 200 de sobreposição para não perder contexto entre blocos
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"✂️ Texto dividido em {len(splits)} blocos")

    # 3. Embeddings & Armazenamento
    # Usamos o modelo do Google para criar os vetores
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)
    
    vectorstore_path = "data/vectorstore"
    
    # Criamos (ou carregamos) o banco Chroma persistente
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=vectorstore_path
    )
    
    print(f"💾 Banco vetorial salvo em: {vectorstore_path}")
    return vectorstore

if __name__ == "__main__":
    # Script para teste manual de ingestão
    mock_pdf = "data/raw/rag_langgraph_mock_dataset.pdf"
    if os.path.exists(mock_pdf):
        ingest_documents(mock_pdf)
    else:
        print(f"❌ Erro: Arquivo {mock_pdf} não encontrado.")
