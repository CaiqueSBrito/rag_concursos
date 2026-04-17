# LangGraph e Workflow

Navegacao: [Indice de estudos](./00_indice_estudos.md) | [Prompt RAG e geracao](./07_prompt_rag_e_geracao.md) | [Workflow detalhado](../03_workflow_detalhado.md)

## Definicao

LangGraph e uma biblioteca para orquestrar fluxos compostos por estado compartilhado e nos executaveis.

No projeto, ele organiza a sequencia de recuperacao e geracao.

## Por que isso importa

Ele separa as etapas do pipeline em partes mais claras:
- estado;
- nos;
- arestas;
- grafo compilado.

## Como isso aparece no projeto

Os arquivos principais relacionados a esse conceito sao:
- [app/graph/state.py](../arquivos/app/graph/state.py.md)
- [app/graph/nodes/retrieve.py](../arquivos/app/graph/nodes/retrieve.py.md)
- [app/graph/nodes/generate.py](../arquivos/app/graph/nodes/generate.py.md)
- [app/graph/workflow.py](../arquivos/app/graph/workflow.py.md)

## Implementacao observada

O workflow atual e linear:
- `START -> retrieve -> generate -> END`

Em termos praticos:
- a API monta um `initial_state`;
- o grafo envia esse estado para `retrieve`;
- `retrieve` preenche `documents`;
- `generate` usa `question` e `documents` para preencher `generation`.

## Como pensar o estado

O ponto central do LangGraph nao e apenas a ordem dos nos. E o fato de que cada etapa trabalha sobre um estado compartilhado.

No projeto atual, esse estado tem:
- `question`
- `documents`
- `generation`

Se o projeto evoluir para um workflow mais robusto, esse estado deve crescer para incluir informacoes como:
- `retrieval_scores`
- `has_relevant_context`
- `fallback_reason`

## Valor didatico no projeto

Esse desenho deixa claro:
- quais dados entram no estado;
- onde o contexto e recuperado;
- onde a resposta e gerada;
- onde a API consome o grafo compilado.

Tambem deixa claro o limite atual: o projeto usa LangGraph mais como pipeline linear do que como motor de decisao.

## Evolucao recomendada

O proximo passo natural do workflow seria:

`START -> retrieve -> validate_context -> generate | fallback -> END`

Esse desenho adiciona decisao e controle de qualidade ao fluxo.

## Leia no projeto

- [Workflow do grafo](../arquivos/app/graph/workflow.py.md)
- [Estado do grafo](../arquivos/app/graph/state.py.md)
- [Workflow e relacoes do projeto](../02_workflow_relacoes.md)
- [Workflow detalhado do projeto RAG](../03_workflow_detalhado.md)
- [Validacao de contexto recuperado](../04_validacao_contexto_recuperado.md)
