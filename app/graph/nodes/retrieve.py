from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.graph.state import GraphState
from app.core.config import settings

from app.graph.nodes.validate_context import validate_context

def retrieve(state: GraphState):
    """
    Nó que recupera documentos do banco vetorial.
    """
    print("🔍 [Nó: Retrieve] Buscando documentos relevantes...")
    
    question = state["question"]
    
    # Inicializa o banco vetorial (mesma configuração da ingestão)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)
    vectorstore = Chroma(persist_directory=settings.VECTORSTORE_PATH, embedding_function=embeddings)
    
    results = vectorstore.similarity_search_with_relevance_scores(question, k=6, score_threshold=0.35)
    documents = [doc for doc, score in results]
    scores = [score for _, score in results]                                                                                                                             

    has_relevant_context = (                                                                                                                                             
      len(documents) > 0                                                                                                                                               
      and max(scores) >= 0.45                                                                                                                                          
      and (sum(scores) / len(scores)) >= 0.40                                                                                                                          
    )

    # Retornamos o dicionário que será mesclado ao estado atual
    return {"documents": documents, "question": question, "has_relevant_context": has_relevant_context}
