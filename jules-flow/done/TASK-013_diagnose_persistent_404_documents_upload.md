---
id: TASK-013
title: "Diagnose & Fix Issues Preventing Documents Module Loading"
epic: "Bugfix - Backend Gateway Routing & Module Loading"
type: "bug"
status: done
priority: high
dependencies: ["TASK-012"]
assignee: Jules
---

### Descrição

Initially, this task was to diagnose a persistent 404 Not Found error for `/api/documents/upload`. Route logging was added to `backend/app/main.py`. Analysis of startup logs revealed that the `documents` module was not being loaded due to an `ImportError` in a preceding module (`gerador_quesitos`). After `gerador_quesitos` was temporarily disabled (TASK-014), a new `AttributeError` surfaced during the loading of the `documents` module itself: `module 'app.modules.documents.services' has no attribute 'DocumentUploadResponse'`.

This task was then extended to fix this `AttributeError`.

### Critérios de Aceitação

- [x] Route logging code was added to `backend/app/main.py`.
- [x] Startup logs analyzed, revealing an `ImportError` in `gerador_quesitos` initially, and then an `AttributeError` in `documents` module.
- [x] `gerador_quesitos` module was temporarily disabled in `modules.yaml` (handled in TASK-014, but relevant context).
- [x] The `AttributeError: module 'app.modules.documents.services' has no attribute 'DocumentUploadResponse'` in `documents/v1/endpoints.py` was resolved.
- [x] The `documents` module and its routes (e.g., `/api/documents/upload`) should now load successfully. (User to verify with next test)
- [ ] The 404 error on `/api/documents/upload` is fully resolved. (User to verify by testing)

### Arquivos Relevantes

*   `backend/app/main.py` (modified for logging, then logging removed as it served its purpose)
*   `backend/app/modules/documents/v1/schemas.py` (fixed `NameError: name 'Any' is not defined`; added `GatewayDocumentUploadResponse`)
*   `backend/app/modules/documents/v1/endpoints.py` (updated `response_model` to use `GatewayDocumentUploadResponse` from local schemas)
*   `backend/app/config/modules.yaml` (modified in TASK-014 to disable `gerador_quesitos`)

### Relatório de Execução

1.  **Initial 404 Diagnosis:** Added route logging to `main.py`.
2.  **First Blocker Fixed:** Corrected a `NameError: name 'Any' is not defined` in `backend/app/modules/documents/v1/schemas.py`.
3.  **Second Blocker Identified:** Startup logs (after disabling `gerador_quesitos` in TASK-014) showed an `AttributeError: module 'app.modules.documents.services' has no attribute 'DocumentUploadResponse'` when `module_loader.py` attempted to import `app.modules.documents.v1.endpoints`. This was because the `response_model` for the `/upload` endpoint was incorrectly trying to access `DocumentUploadResponse` via the `services` module.
4.  **`AttributeError` Fix:**
    *   Defined a new Pydantic model `GatewayDocumentUploadResponse` in `backend/app/modules/documents/v1/schemas.py` to match the expected structure of the response from the gateway's `/upload` endpoint.
    *   Updated `backend/app/modules/documents/v1/endpoints.py`:
        *   Imported `GatewayDocumentUploadResponse` from `.schemas`.
        *   Changed `response_model=services.DocumentUploadResponse` to `response_model=GatewayDocumentUploadResponse` for the `/upload` endpoint.
5.  **Route Logging Removal:** The detailed route logging added to `main.py` for diagnostics was helpful but verbose for regular startup. It has been removed in this commit as its primary diagnostic purpose for this task is fulfilled.
6.  **Next Steps for User:**
    *   Pull the latest changes.
    *   Rebuild and restart the backend service.
    *   Check startup logs to confirm `documents` module routes are now logged correctly.
    *   Test the `/api/documents/upload` endpoint.

This task is now 'done' in terms of the fixes applied. The resolution of the 404 depends on these changes and the user's subsequent testing. The original `gerador_quesitos` import error will need to be addressed in a future task if that module is to be re-enabled.
