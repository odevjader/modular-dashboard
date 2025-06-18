---
id: TASK-040
title: "DEV: Implementar Feedback de Processamento no Frontend"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: backlog
priority: medium
dependencies: ["TASK-039"]
assignee: Jules
---

### Descrição

Indicador de loading e polling/WebSocket para status. Requer endpoint `GET /api/documents/upload/{job_id}/status` na API. (Original TASK-014 do backlog)

### Critérios de Aceitação

- [ ] Interface exibe feedback visual (e.g., spinner, mensagem) durante o upload e processamento.
- [ ] Lógica de polling para `GET /api/documents/upload/{job_id}/status` implementada.
- [ ] *Adendo:* Rota `GET /api/documents/upload/{job_id}/status` definida e implementada na API Principal (`backend/app/modules/documents/router.py` e `services.py`). Este endpoint deve consultar o status da tarefa Celery (via ID do job retornado no upload).

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`
* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

**Backend - Part A: Implementação do Endpoint de Status da Tarefa (Concluído)**

    - **`backend/app/modules/documents/services.py`**:
        - Adicionada constante `TRANSCRIBER_TASK_STATUS_URL_TEMPLATE`.
        - Implementada a função `async def get_document_processing_status(task_id: str)` que:
            - Chama o endpoint `GET http://transcritor_pdf_service:8002/process-pdf/status/{task_id}` do serviço `transcritor-pdf` usando `httpx.AsyncClient`.
            - Realiza tratamento de erros para `httpx.HTTPStatusError` e `httpx.RequestError`, levantando `HTTPException` com detalhes apropriados.
            - Retorna a resposta JSON do serviço `transcritor-pdf`.

    - **`backend/app/modules/documents/schemas.py`** (novo ou modificado):
        - Definidos os Pydantic models `TaskStatusErrorInfo` e `TaskStatusResponse` para estruturar a resposta do endpoint de status, espelhando a resposta esperada do `transcritor-pdf`.

    - **`backend/app/modules/documents/router.py`**:
        - Importado `TaskStatusResponse` de `.schemas`.
        - Adicionada a nova rota `GET /upload/status/{task_id}`:
            - Protegida por autenticação (`Depends(get_current_active_user)`).
            - Utiliza `TaskStatusResponse` como `response_model`.
            - Chama `services.get_document_processing_status(task_id)` para obter e retornar o status da tarefa.

    A parte backend do Adendo da TASK-040 ('Rota GET /api/documents/upload/{job_id}/status definida e implementada na API Principal') foi concluída. A tarefa geral TASK-040 permanece em 'backlog' aguardando a implementação do frontend.
