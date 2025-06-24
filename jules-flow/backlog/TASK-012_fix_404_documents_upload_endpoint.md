---
id: TASK-012
title: "Fix 404 Not Found for /api/documents/upload Endpoint"
epic: "Bugfix - Backend Gateway Routing"
type: "bug"
status: backlog
priority: high
dependencies: ["TASK-007", "TASK-011"] # Depends on frontend tester and attempted backend fixes
assignee: Jules
---

### Descrição

After recent changes, the frontend is receiving a 404 Not Found error when attempting to POST to the `/api/documents/upload` endpoint. The backend gateway service (FastAPI application in `backend/app/`) is not recognizing this route.

This task is to investigate the routing configuration within the backend gateway, specifically how the `documents` module router (from `backend/app/modules/documents/endpoints.py`) is included in the main FastAPI application (`backend/app/main.py` or `backend/app/api_router.py`), and correct any misconfiguration.

### Critérios de Aceitação

- [ ] The root cause of the 404 error for `/api/documents/upload` is identified.
- [ ] The routing configuration in the backend gateway service is corrected.
- [ ] The `/api/documents/upload` endpoint is reachable and returns a non-404 status when called (e.g., a 2xx success or a different error if subsequent processing fails, but not a 404 for the route itself).
- [ ] PDF upload functionality can proceed past the 404 error stage.

### Arquivos Relevantes

* `backend/app/main.py` (main FastAPI application)
* `backend/app/api_router.py` (if it exists and is used for routing)
* `backend/app/modules/documents/endpoints.py` (defines the `/upload` endpoint)
* `frontend/vite.config.ts` (for proxy review, though likely not the issue here)
* `frontend/src/services/api.ts` (for reviewing the called URL)

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
