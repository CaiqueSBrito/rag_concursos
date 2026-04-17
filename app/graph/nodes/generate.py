from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.core.config import settings

def generate(state: GraphState):
    """
    Nó que gera uma resposta baseada no contexto recuperado.
    """
    print("✍️ [Nó: Generate] Gerando resposta com Gemini...")
    
    question = state["question"]
    documents = state["documents"]
    
    # Concatenamos o conteúdo dos documentos encontrados
    context = "\n\n".join([doc.page_content for doc in documents])
    
    # Definimos o Prompt de RAG
    template = """Você é um assistente especializado em responder perguntas com base em documentos técnicos.
    
    Use APENAS o contexto fornecido abaixo para responder a pergunta. 
    Se a resposta não estiver no contexto, diga apenas que não tem informação suficiente.
    Seja preciso e profissional.

    CONTEXTO:
    {context}

    PERGUNTA:
    {question}

    RESPOSTA:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Inicializamos o Gemini (LLM)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7 # Criatividade balanceada
    )
    
    # Criamos a chain e invocamos
    rag_chain = prompt | llm
    response = rag_chain.invoke({"context": context, "question": question})
    
    return {"generation": response.content}
