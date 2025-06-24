---
id: TASK-013
title: "Diagnose Persistent 404 Error for /api/documents/upload"
epic: "Bugfix - Backend Gateway Routing"
type: "bug"
status: done # Updated status
priority: high
dependencies: ["TASK-012"]
assignee: Jules
---

### Descrição

Despite fixes applied in TASK-012 (creating `app/modules/__init__.py` and refactoring the `documents` module structure), the frontend continued to receive a 404 Not Found error when POSTing to `/api/documents/upload`. This task involved adding route logging to `backend/app/main.py` to inspect all registered routes.

### Critérios de Aceitação

- [x] Route logging code was added to `backend/app/main.py`.
- [x] User ran the backend and provided the startup logs.
- [x] Analysis of the logged routes revealed that the `documents` module (and `gerador_quesitos`) was not being loaded due to an `ImportError` in `gerador_quesitos` (`cannot import name 'logger' from 'app.core.config'`).
- [x] A clear path to resolving the 404 was determined: fix the `ImportError` in `gerador_quesitos` to allow all modules to load correctly. This will be handled in TASK-014.

### Arquivos Relevantes

* `backend/app/main.py` (modified for logging)
* `backend/app/modules/documents/v1/schemas.py` (fixed NameError for `Any` during this task's investigation)
* `backend/app/core/module_loader.py` (reviewed)
* `backend/app/config/modules.yaml` (reviewed)
* `backend/app/modules/gerador_quesitos/v1/endpoints.py` (identified as source of new ImportError)

### Relatório de Execução

1.  **Added Route Logging:** Modified `backend/app/main.py` to log all registered FastAPI routes at startup.
2.  **Fixed Prerequisite `NameError`:** Corrected a `NameError: name 'Any' is not defined` in `backend/app/modules/documents/v1/schemas.py` by adding `from typing import Any`. This allowed the module loader to proceed further.
3.  **Analyzed Startup Logs:** User provided startup logs. These logs showed:
    *   The `documents` module routes (including `/api/documents/upload`) were **still missing**.
    *   A new `ImportError` was occurring during the loading of the `gerador_quesitos` module: `cannot import name 'logger' from 'app.core.config'`.
    *   The module loader log indicated only 3 modules were successfully loaded, meaning the process was interrupted before loading `documents` (which comes after `gerador_quesitos` in `modules.yaml`).
4.  **Conclusion:** The persistent 404 for `/api/documents/upload` is due to the `ImportError` in the `gerador_quesitos` module, which prevents the `documents` module from being loaded and its routes registered.
5.  **Next Step:** A new task, TASK-014, will be created to fix the `ImportError` in the `gerador_quesitos` module.

This diagnostic task is now complete. The root cause of the persistent 404 (after initial fixes) has been identified.
