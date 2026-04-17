# Retrieval

Navegacao: [Indice de estudos](./00_indice_estudos.md) | [Vectorstore Chroma](./05_vectorstore_chroma.md) | [Prompt RAG e geracao](./07_prompt_rag_e_geracao.md)

## Definicao

Retrieval e a etapa em que o sistema consulta a base vetorial para encontrar os trechos mais relevantes para uma pergunta.

## Papel no projeto

No projeto atual, isso ocorre em [app/graph/nodes/retrieve.py](../arquivos/app/graph/nodes/retrieve.py.md).

A funcao do no e:
- receber a `question`;
- reconstruir o acesso ao Chroma persistido;
- executar a busca semantica;
- devolver os `documents` para o estado do workflow.

## O que acontece no codigo

A etapa de retrieval depende de 3 elementos:
- embeddings compativeis com a base indexada;
- diretorio de persistencia do Chroma;
- consulta textual do usuario.

Hoje a busca e feita com `similarity_search(question, k=4)`.

## Limite tecnico importante

`similarity_search` retorna os documentos mais parecidos, mas nao prova por si so que o contexto e suficiente para responder a pergunta com seguranca.

Por isso, em sistemas RAG mais confiaveis, retrieval e validacao de contexto devem ser tratados como etapas distintas.

## Evolucao recomendada

Uma melhoria importante e usar score explicito de relevancia com `similarity_search_with_relevance_scores`, registrar os scores no estado e adicionar um no `validate_context` antes da geracao.

Essa parte foi detalhada em [Validacao de contexto recuperado](../04_validacao_contexto_recuperado.md).

## Leia no projeto

- [No `retrieve.py`](../arquivos/app/graph/nodes/retrieve.py.md)
- [Workflow do grafo](../arquivos/app/graph/workflow.py.md)
- [Workflow detalhado do projeto RAG](../03_workflow_detalhado.md)
- [Validacao de contexto recuperado](../04_validacao_contexto_recuperado.md)
