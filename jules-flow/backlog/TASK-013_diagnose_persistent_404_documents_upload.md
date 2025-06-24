---
id: TASK-013
title: "Diagnose Persistent 404 Error for /api/documents/upload"
epic: "Bugfix - Backend Gateway Routing"
type: "bug"
status: backlog
priority: high
dependencies: ["TASK-012"] # Follows up on the previous attempt to fix 404
assignee: Jules
---

### Descrição

Despite fixes applied in TASK-012 (creating `app/modules/__init__.py` and refactoring the `documents` module structure), the frontend continues to receive a 404 Not Found error when POSTing to `/api/documents/upload`.

This task is to further diagnose the routing issue by adding detailed route logging to `backend/app/main.py`. This will help inspect all routes registered with the FastAPI application at startup to confirm if `/api/documents/upload` is correctly configured and available.

### Critérios de Aceitação

- [ ] Route logging code is added to `backend/app/main.py`.
- [ ] User runs the backend and provides the startup logs containing the list of all registered routes.
- [ ] Analysis of the logged routes reveals whether `/api/documents/upload` is present and correctly formed, or identifies the misconfiguration.
- [ ] A clear path to resolving the 404 is determined based on the logged routes.

### Arquivos Relevantes

* `backend/app/main.py` (to be modified for logging)
* `backend/app/api_router.py`
* `backend/app/core/module_loader.py`
* `backend/app/config/modules.yaml`
* `backend/app/modules/documents/v1/endpoints.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
