---
id: TASK-040
title: "DEV: Implementar Feedback de Processamento no Frontend"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: done
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

**Frontend - Part B: Implementação do Feedback de Processamento (Concluído)**

    - **`frontend/src/services/api.ts`**:
        - Definidas as interfaces `TaskStatusErrorInfo` e `TaskStatusResponse` para tipar a resposta do endpoint de status.
        - Criada a função `getDocumentProcessingStatus(taskId: string)` que chama o endpoint de gateway `GET /api/documents/upload/status/{taskId}`.

    - **`frontend/src/modules/analisador_documentos/stores/analisadorStore.ts`** (novo arquivo):
        - Criado um store Zustand (`useAnalisadorStore`) para gerenciar o estado do Analisador de Documentos.
        - O estado inclui `currentTaskId`, `status` (com tipos como 'idle', 'uploading', 'processing', 'success', 'error', 'queued'), `progress`, `statusMessage`, `errorMessage`, `processedDocumentId` e `pollingTimerId`.
        - Actions implementadas: `resetState`, `setUploading`, `setUploadSuccess` (que inicia o polling), `_pollStatus` (lógica de polling recursiva com `setTimeout`), e `stopPolling`.
        - A action `_pollStatus` mapeia os status do Celery (recebidos do backend) para os status do frontend.

    - **`frontend/src/modules/analisador_documentos/components/ProcessingStatusIndicator.tsx`** (novo arquivo):
        - Componente React que se inscreve ao `useAnalisadorStore`.
        - Exibe mensagens de status, uma barra de progresso (MUI `LinearProgress` baseada no estado `progress` e `status`) e alertas de erro.

    - **`frontend/src/modules/analisador_documentos/components/DocumentUploadForm.tsx`**:
        - Modificado para interagir com o `useAnalisadorStore`.
        - Chama actions do store (`resetState`, `setUploading`, `setUploadSuccess`) para gerenciar o ciclo de vida do upload e iniciar o polling. Mensagens de feedback e task ID são agora gerenciadas pelo store.

    - **`frontend/src/pages/AnalisadorDocumentosPage.tsx`**:
        - O componente `ProcessingStatusIndicator` foi importado e integrado para exibir o feedback de processamento.

    Com a conclusão da parte frontend, a TASK-040 está integralmente finalizada. O sistema agora possui feedback visual e polling para o status de processamento de documentos.
