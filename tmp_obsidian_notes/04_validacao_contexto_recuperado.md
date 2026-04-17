# Validacao de Contexto Recuperado

Navegacao: [Indice](./00_indice.md) | [Workflow detalhado](./03_workflow_detalhado.md) | [Retrieval](./estudos/06_retrieval.md)

## Objetivo desta nota

Esta nota explica como verificar se o contexto recuperado pelo `similarity_search` e suficientemente relevante antes de envia-lo para o prompt final.

A pergunta central e:

`como evitar que o generate responda com base em chunks pouco relevantes ou insuficientes?`

## Problema no desenho atual

No projeto atual, o no [app/graph/nodes/retrieve.py](./arquivos/app/graph/nodes/retrieve.py.md) usa `similarity_search(question, k=4)` e devolve diretamente os documentos para [app/graph/nodes/generate.py](./arquivos/app/graph/nodes/generate.py.md).

Esse desenho tem uma fragilidade importante: o workflow assume que o top `k` retornado pelo vectorstore ja e contexto valido. Isso nem sempre e verdade.

Alguns cenarios comuns de falso positivo:
- o embedding encontra chunks semanticamente proximos, mas incompletos;
- os chunks tratam de um assunto relacionado, mas nao respondem a pergunta especifica;
- os documentos recuperados sao pouco informativos;
- a base vetorial esta vazia, inconsistente ou muito pequena.

## O que validar

Uma verificacao robusta precisa responder pelo menos 3 perguntas:
- os chunks recuperados sao parecidos com a pergunta?
- o conjunto recuperado e suficiente para responder com seguranca?
- vale a pena seguir para `generate` ou o fluxo deve parar em fallback?

## Opcao 1: validacao objetiva por score

A forma mais direta e trocar `similarity_search` por `similarity_search_with_relevance_scores`.

Nesta instalacao, o `Chroma` expoe esse metodo e a propria docstring indica:
- score no intervalo `0..1`;
- `0` significa dissimilar;
- `1` significa mais similar;
- `score_threshold` pode ser usado para filtrar resultados.

Exemplo conceitual de retrieval com score:

```python
results = vectorstore.similarity_search_with_relevance_scores(
    question,
    k=6,
    score_threshold=0.35,
)

documents = [doc for doc, score in results]
scores = [score for _, score in results]
```

## Como interpretar os scores

Os scores nao devem ser usados de forma isolada. O ideal e combinar criterios.

Exemplo de regra pratica:
- rejeitar se nenhum documento for retornado;
- rejeitar se `max_score < 0.45`;
- rejeitar se `media(scores) < 0.40`;
- aprovar apenas se houver quantidade e qualidade minima de contexto.

Exemplo:

```python
has_relevant_context = (
    len(documents) > 0
    and max(scores) >= 0.45
    and (sum(scores) / len(scores)) >= 0.40
)
```

Esses thresholds sao apenas ponto de partida. O valor correto depende do seu corpus, da granularidade dos chunks e da distribuicao real dos embeddings.

## Opcao 2: no de validacao no LangGraph

A melhor forma de encaixar isso no projeto e adicionar um no intermediario ao workflow.

Desenho sugerido:

`START -> retrieve -> validate_context -> generate | fallback -> END`

Nesse modelo:
- `retrieve` recupera documentos e scores;
- `validate_context` decide se o contexto e suficiente;
- `generate` so executa quando `has_relevant_context` for verdadeiro;
- `fallback` responde que nao ha informacao suficiente ou confiavel.

## Como o estado deve evoluir

Hoje o estado tem apenas:
- `question`
- `documents`
- `generation`

Para suportar validacao, o estado deveria ganhar pelo menos:
- `retrieval_scores`
- `has_relevant_context`

Exemplo conceitual:

```python
class GraphState(TypedDict):
    question: str
    documents: List[Document]
    retrieval_scores: List[float]
    has_relevant_context: bool
    generation: str
```

## Exemplo de no `validate_context`

```python
def validate_context(state: GraphState):
    documents = state["documents"]
    scores = state["retrieval_scores"]

    if not documents or not scores:
        return {"has_relevant_context": False}

    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    has_relevant_context = max_score >= 0.45 and avg_score >= 0.40
    return {"has_relevant_context": has_relevant_context}
```

Esse no nao gera texto. Ele apenas protege a etapa de geracao.

## Exemplo de fluxo condicional

Em LangGraph, o proximo passo pode ser escolhido com aresta condicional.

Exemplo conceitual:

```python
workflow.add_conditional_edges(
    "validate_context",
    lambda state: "generate" if state["has_relevant_context"] else "fallback"
)
```

Esse detalhe e importante porque muda a funcao do workflow. Em vez de ser um pipeline cego, ele passa a ser um orquestrador com controle de qualidade.

## Opcao 3: validacao semantica por LLM grader

Se o score vetorial nao for suficiente, uma segunda camada pode ser adicionada: um `grader` com LLM.

Nesse caso, o sistema pergunta a outro prompt algo como:
- o contexto recuperado contem informacao suficiente para responder sem inferencia externa?
- quais chunks sao realmente uteis para a pergunta?

Vantagens:
- melhor filtragem semantica quando o embedding recupera texto relacionado, mas insuficiente;
- reduz falso positivo em perguntas especificas.

Custos:
- maior latencia;
- maior custo de inferencia;
- risco de introduzir variabilidade adicional se o grader nao for bem restringido.

## Ordem recomendada de implementacao

Para este projeto, a ordem pragmatica seria:
1. trocar `similarity_search` por `similarity_search_with_relevance_scores`;
2. salvar os scores no estado;
3. criar `validate_context`;
4. adicionar um no `fallback`;
5. so depois avaliar se vale incluir um grader com LLM.

Essa ordem entrega ganho real de confiabilidade sem complicar demais o fluxo.

## Regra operacional recomendada

Uma politica simples e segura seria:
- se nenhum chunk relevante for encontrado, nao gerar resposta factual;
- se os scores forem baixos, retornar que nao ha informacao suficiente no contexto recuperado;
- se o contexto for aprovado, seguir para o `generate`;
- se necessario, registrar scores e documentos no log para calibracao futura.

## Como isso se conecta ao prompt

A validacao de contexto existe para proteger o prompt final.

Sem essa etapa, o prompt em [app/graph/nodes/generate.py](./arquivos/app/graph/nodes/generate.py.md) recebe qualquer contexto retornado pelo vectorstore. Isso cria um risco estrutural: o modelo pode produzir uma resposta articulada sobre um contexto apenas parcialmente relacionado.

Com a validacao:
- o prompt recebe um contexto com criterio minimo de relevancia;
- o sistema passa a responder menos vezes, mas com base mais defensavel;
- a taxa de alucinacao tende a cair.

## Resumo tecnico

A verificacao de relevancia do contexto deve acontecer antes da geracao. O mecanismo mais objetivo e usar score de retrieval, limiar minimo e um no de validacao no LangGraph.

Em termos de arquitetura, a pergunta correta deixa de ser `recuperei algum chunk?` e passa a ser `recuperei contexto suficiente para responder com seguranca?`

## Notas relacionadas

- [Workflow detalhado do projeto RAG](./03_workflow_detalhado.md)
- [Workflow e relacoes do projeto](./02_workflow_relacoes.md)
- [Retrieval](./estudos/06_retrieval.md)
- [Prompt RAG e geracao](./estudos/07_prompt_rag_e_geracao.md)
- [LangGraph e Workflow](./estudos/08_langgraph_e_workflow.md)
