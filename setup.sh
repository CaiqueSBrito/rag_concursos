#!/bin/bash

echo "🚀 Iniciando preparação do ambiente RAG com FastAPI e LangGraph..."

# Atualizando o pip
echo "📦 Atualizando pip..."
python -m pip install --upgrade pip

# Instalação das dependências do FastAPI e utilitários da Web
echo "🌐 Instalando FastAPI, Uvicorn e utilitários..."
pip install fastapi uvicorn[standard] python-dotenv pydantic python-multipart

# Instalação do ecossistema LangGraph e LangChain
echo "🧠 Instalando LangGraph, LangChain, ferramentas de Embeddings e Parsing..."
pip install langgraph langgraph-checkpoint-sqlite langchain langchain-core langchain-community langchain-openai langchain-huggingface
pip install pypdf tiktoken unstructured sentence-transformers

# Instalação do Banco de Dados Vetorial (ChromaDB para armazenamento local fácil)
echo "💾 Instalando ChromaDB (Vector Database)..."
pip install chromadb

# Criando a estrutura de pastas adaptada para o LangGraph Workflow
echo "📁 Criando estrutura de repositórios..."

mkdir -p app/api/endpoints
mkdir -p app/core
mkdir -p app/services
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/graph/nodes    # Para os nós do ciclo (Retrieval, Generation, Grading)
mkdir -p app/graph/routes   # Para a lógica do fluxo condicional (Routing)
mkdir -p data/raw          # Documentos PDF/Txt originais
mkdir -p data/vectorstore  # Onde o ChromaDB vai salvar os dados vetoriais localmente

# Criando arquivos fundamentais iniciais
touch app/__init__.py
touch app/main.py
touch app/core/config.py
touch app/graph/__init__.py
touch app/graph/state.py    # Para o a estrutura TypedDict do LangGraph State
touch app/graph/workflow.py # Onde será definido o compiled graph
touch .env
touch requirements.txt

# Guardando o estado das dependências no requirements
pip freeze > requirements.txt

echo "✅ Ambiente preparado com sucesso! Você está pronto para construir o RAG com Automação Orientada a Grafos (LangGraph)."
