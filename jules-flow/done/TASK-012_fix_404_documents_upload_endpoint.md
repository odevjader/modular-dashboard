---
id: TASK-012
title: "Fix 404 Not Found for /api/documents/upload Endpoint"
epic: "Bugfix - Backend Gateway Routing"
type: "bug"
status: done
priority: high
dependencies: ["TASK-007", "TASK-011"]
assignee: Jules
---

### Descrição

The frontend was receiving a 404 Not Found error when attempting to POST to the `/api/documents/upload` endpoint. The backend gateway service was not recognizing this route. Investigation focused on the `documents` module's structure and its registration with the dynamic module loader.

### Critérios de Aceitação

- [x] The root cause of the 404 error for `/api/documents/upload` was identified.
- [x] The routing configuration and module structure for the `documents` module in the backend gateway service was corrected.
- [x] The `/api/documents/upload` endpoint is now reachable (confirmed by user that subsequent errors like 307 and 401 occurred, indicating the route itself was found).
- [x] PDF upload functionality can proceed past the 404 error stage.

### Arquivos Relevantes

*   `backend/app/main.py` (reviewed)
*   `backend/app/api_router.py` (reviewed)
*   `backend/app/core/module_loader.py` (reviewed)
*   `backend/app/config/modules.yaml` (modified)
*   `backend/app/modules/documents/endpoints.py` (deleted)
*   `backend/app/modules/documents/schemas.py` (deleted)
*   `backend/app/modules/documents/v1/endpoints.py` (created/modified to consolidate endpoints)
*   `backend/app/modules/documents/v1/schemas.py` (modified to consolidate schemas)
*   `backend/app/modules/__init__.py` (created)

### Relatório de Execução

1.  **Initial Investigation:** Confirmed the 404 error on `/api/documents/upload`.
2.  **Missing Package Init:** Identified that `backend/app/modules/__init__.py` was missing. Created this file to allow `app.modules` to be treated as a package, enabling proper import of submodules like `documents`. This was an initial attempt to fix the issue.
3.  **Module Structure Misalignment:** User reported the 404 persisted. Further investigation revealed that the `documents` module structure was inconsistent with other versioned modules (e.g., `info`, `gerador_quesitos`) that were being loaded correctly by `module_loader.py`. The `documents` module had its main endpoints at the top level (`modules/documents/endpoints.py`) while also having a `v1` subdirectory.
4.  **Refactoring `documents` Module:**
    *   Consolidated all endpoint definitions (e.g., `/upload`, `/query/{document_id}`, `/upload/status/{task_id}`) into `backend/app/modules/documents/v1/endpoints.py`. The `APIRouter` instance in this file was named `router`.
    *   Moved relevant Pydantic schemas from `backend/app/modules/documents/schemas.py` to `backend/app/modules/documents/v1/schemas.py`.
    *   Deleted the now redundant `backend/app/modules/documents/endpoints.py` and `backend/app/modules/documents/schemas.py`.
5.  **Updated `modules.yaml`:**
    *   Modified the entry for the `documents` module:
        *   `path` changed from `modules.documents` to `modules.documents.v1`.
        *   `router_variable_name` changed from `api_router` to `router`.
        *   `tags` updated to `["Documents v1"]`.
        *   The `prefix` remained `/documents`. The module loader uses this prefix, and the main app router adds `/api`, making the effective path for `/upload` in `v1/endpoints.py` become `/api/documents/upload`.
6.  **Verification:** After these refactoring changes, the user's subsequent reports of 307 and 401 errors on the `/api/documents/upload` path confirmed that the 404 "Not Found" error was resolved, as the application was now routing the request to the correct endpoint handler.

This task is now considered complete as the 404 error has been addressed by correcting the module structure and its registration. Subsequent errors (307, 401) were handled in TASK-008, TASK-009, and TASK-011.
