---
id: TASK-032
title: "DEV: Expandir Gateway na API Principal para Diálogo"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-029", "TASK-014"] # Depends on transcritor dialog endpoint and API documents module
assignee: Jules
---

### Descrição

Rota `POST /api/documents/query/{document_id}` na API principal, chamando endpoint do `transcritor-pdf`. (Original TASK-011 do backlog)

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/query/{document_id}` implementada em `backend/app/modules/documents/router.py`.
- [ ] Rota requer autenticação.
- [ ] Aceita pergunta do usuário.
- [ ] `documents/services.py` chama `http://transcritor_pdf_service:8002/query-document/{document_id}`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

Implementada a rota `POST /api/documents/query/{document_id}` em `backend/app/modules/documents/router.py`.
    - A rota utiliza o Pydantic model `DocumentQueryRequest` para aceitar `user_query` no corpo da requisição.
    - A autenticação de usuário é verificada através de `get_current_active_user`.
    - Uma nova função `handle_document_query` foi adicionada em `backend/app/modules/documents/services.py`.
    - Esta função `handle_document_query` chama o endpoint `POST http://transcritor_pdf_service:8002/query-document/{document_id}` do serviço `transcritor-pdf`, encaminhando a `user_query`.
    - Foram incluídos tratamentos de erro para chamadas ao serviço externo e validação básica da query.
    Os critérios de aceitação foram atendidos.
