---
id: TASK-029
title: "DEV: Criar Endpoint de Diálogo no Transcritor-PDF"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-026"] # Depende do orquestrador de respostas
assignee: Jules
---

### Descrição

Rota `POST /query-document/{document_id}` em `transcritor-pdf/src/main.py`. (Original TASK-010 do backlog)

### Critérios de Aceitação

- [x] Rota `POST /query-document/{document_id}` implementada em `transcritor-pdf/src/main.py`.
- [x] Aceita JSON com pergunta do usuário.
- [x] Chama o orquestrador de respostas (TASK-026).
- [x] Retorna a resposta gerada.

### Arquivos Relevantes

* `transcritor-pdf/src/main.py`

### Relatório de Execução

- Implemented the `POST /query-document/{document_id}` endpoint in `transcritor-pdf/src/main.py`.
- Defined a Pydantic model `UserQueryRequest` for the request body, expecting `{"user_query": "..."}`.
- The endpoint calls `get_llm_answer_with_context` from `src.query_processor`, passing the `user_query` and using `document_id` as the `document_filename` for context retrieval.
- The response from `get_llm_answer_with_context` (a dictionary containing the answer, retrieved context, and any error) is returned by the endpoint.
- Added OpenAPI documentation (summary, description, tags) for the new endpoint.
- Verified the logical flow of the implementation and documented a sample `curl` command for testing.
