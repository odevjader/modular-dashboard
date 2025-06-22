---
id: TASK-013
title: "DEV: Implementar Endpoint de Upload no Módulo `documents`"
epic: "Fase 2: Implementação do Gateway de Comunicação na API Principal"
status: done
priority: medium
dependencies: ["TASK-010", "TASK-012"] # Depends on module structure and its tests
assignee: Jules
---

### Descrição

Rota `POST /upload` autenticada, aceitando `UploadFile`. Serviço para repassar o arquivo ao `transcritor-pdf` (endpoint `http://transcritor_pdf_service:8002/process-pdf`). (Original TASK-006 do backlog)

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/upload` implementada em `documents/router.py`.
- [ ] Rota usa `Depends(get_current_active_user)`.
- [ ] Aceita `UploadFile`.
- [ ] `documents/services.py` contém lógica para encaminhar o request para `http://transcritor_pdf_service:8002/process-pdf`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

Implementation successfully completed.

1.  **Endpoint**: Created `POST /api/documents/upload` in `backend/app/modules/documents/router.py`.
    *   Secured with `Depends(get_current_active_user)`.
    *   Accepts `UploadFile`.
    *   Calls the corresponding service function.

2.  **Service**: Implemented `handle_file_upload(file: UploadFile, user_id: int)` in `backend/app/modules/documents/services.py`.
    *   Uses `httpx.AsyncClient` to make an asynchronous `POST` request to `http://transcritor_pdf_service:8002/process-pdf`.
    *   Sends the file content (as `upload_file`) and `user_id` as multipart form data.
    *   Includes error handling for HTTP status errors (from transcriber) and request/connection errors.
    *   Ensures `file.close()` is called.

3.  **Unit Tests**: Added in `backend/tests/test_documents_module.py`.
    *   Removed outdated `test_import_document_services`.
    *   Mocked `get_current_active_user` for authentication.
    *   Mocked `httpx.AsyncClient.post` to isolate tests from the external transcriber service.
    *   Test cases cover:
        *   Successful upload and response.
        *   Errors from the transcriber service (HTTPStatusError, e.g., 422, 500).
        *   Connection errors to the transcriber service (RequestError, resulting in 503).
        *   Unexpected exceptions during the service call (resulting in 500).
    *   Updated `test_documents_module_router_integration` to check for the new upload route in OpenAPI spec.

The solution adheres to the requirements, providing a functional and tested upload endpoint.
