# Documentacao do Projeto RAG

## Visao geral

Este conjunto de notas documenta o projeto localizado em `C:\Users\gamer\Documents\projetos_python\projetos fast_api\RAG`.

A documentacao foi organizada para facilitar tres objetivos:
- entender a arquitetura atual do projeto;
- navegar por cada arquivo com explicacao tecnica objetiva;
- enxergar a relacao entre ingestao, recuperacao, geracao e exposicao da API.

Foram documentados os arquivos de codigo, configuracao e suporte relevantes do projeto.
O diretorio `venv` foi excluido por ser ambiente gerado localmente.
O diretorio `data/vectorstore` aparece no mapa estrutural, mas nao recebeu nota por arquivo porque ele e um artefato de runtime e nao continha arquivos-fonte nesta varredura.

## Navegacao principal

- [Trilha de estudos de RAG](./estudos/00_indice_estudos.md)
- [Workflow e relacoes do projeto](./02_workflow_relacoes.md)
- [Workflow detalhado do projeto RAG](./03_workflow_detalhado.md)
- [Validacao de contexto recuperado](./04_validacao_contexto_recuperado.md)
- [Estrutura do projeto e links](./01_estrutura_e_links.md)
- [Arquivo de ambiente `.env`](./arquivos/raiz/env.md)
- [Dependencias em `requirements.txt`](./arquivos/raiz/requirements.txt.md)
- [Script de bootstrap `setup.sh`](./arquivos/raiz/setup.sh.md)
- [Pacote `app/__init__.py`](./arquivos/app/__init__.py.md)
- [Aplicacao FastAPI `app/main.py`](./arquivos/app/main.py.md)
- [Endpoint HTTP `app/api/endpoints/chat.py`](./arquivos/app/api/endpoints/chat.py.md)
- [Configuracoes `app/core/config.py`](./arquivos/app/core/config.py.md)
- [Pacote do grafo `app/graph/__init__.py`](./arquivos/app/graph/__init__.py.md)
- [Estado compartilhado `app/graph/state.py`](./arquivos/app/graph/state.py.md)
- [Workflow do LangGraph `app/graph/workflow.py`](./arquivos/app/graph/workflow.py.md)
- [No de recuperacao `app/graph/nodes/retrieve.py`](./arquivos/app/graph/nodes/retrieve.py.md)
- [No de geracao `app/graph/nodes/generate.py`](./arquivos/app/graph/nodes/generate.py.md)
- [Servico de ingestao `app/services/ingestion_service.py`](./arquivos/app/services/ingestion_service.py.md)
- [Arquivo de entrada `data/raw/rag_langgraph_mock_dataset.pdf`](./arquivos/data/raw/rag_langgraph_mock_dataset.pdf.md)

## Fluxo recomendado de leitura

1. Comece por [estrutura e links](./01_estrutura_e_links.md).
2. Leia [config.py](./arquivos/app/core/config.py.md) para entender como o projeto resolve parametros.
3. Passe por [ingestion_service.py](./arquivos/app/services/ingestion_service.py.md) para ver como o vetor e criado.
4. Em seguida leia [state.py](./arquivos/app/graph/state.py.md), [retrieve.py](./arquivos/app/graph/nodes/retrieve.py.md), [generate.py](./arquivos/app/graph/nodes/generate.py.md) e [workflow.py](./arquivos/app/graph/workflow.py.md).
5. Aprofunde em [Workflow detalhado do projeto RAG](./03_workflow_detalhado.md) e [Validacao de contexto recuperado](./04_validacao_contexto_recuperado.md).
6. Feche o fluxo com [chat.py](./arquivos/app/api/endpoints/chat.py.md) e [main.py](./arquivos/app/main.py.md).

## Observacoes gerais

- A arquitetura implementada se aproxima de um RAG minimo com FastAPI, LangGraph, Chroma e Gemini.
- Existem diretorios previstos para expansao (`models`, `schemas`, `graph/routes`) que ainda nao possuem implementacao concreta.
- Ha um desalinhamento importante entre o nome da variavel no `.env` e a configuracao lida em `config.py`; isso foi destacado nas notas especificas.
- O workflow atual e linear; as novas notas detalham como evoluir para uma validacao explicita de contexto antes da geracao.
