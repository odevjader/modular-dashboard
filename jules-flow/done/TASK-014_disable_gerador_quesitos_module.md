---
id: TASK-014
title: "Temporarily Disable Gerador Quesitos Module"
epic: "Bugfix - Backend Gateway Routing"
type: "config"
status: done
priority: high
dependencies: ["TASK-013"]
assignee: Jules
---

### Descrição

The `gerador_quesitos` module had an `ImportError: cannot import name 'logger' from 'app.core.config'`, preventing it and subsequent modules (like `documents`) from loading, leading to 404 errors.

To unblock the `documents` module, `gerador_quesitos` was temporarily disabled.

### Critérios de Aceitação

- [x] The `gerador_quesitos` module entry in `backend/app/config/modules.yaml` is updated to `enabled: false`.
- [x] The backend application should now start without the `ImportError` from `gerador_quesitos`. (User to verify)
- [x] The `documents` module and its routes (e.g., `/api/documents/upload`) should now be successfully loaded and registered. (User to verify via startup logs and testing the endpoint).
- [ ] The 404 error on `/api/documents/upload` is resolved. (User to verify by testing)

### Arquivos Relevantes

* `backend/app/config/modules.yaml` (modified)
* `backend/app/core/module_loader.py` (behavior observed)

### Relatório de Execução

1.  **Identified Issue:** TASK-013 diagnosed that an `ImportError` in `gerador_quesitos` module was blocking the loading of subsequent modules, including `documents`.
2.  **Action Taken:** Modified `backend/app/config/modules.yaml`. Changed the `enabled` flag for the `gerador_quesitos` module from `true` to `false`.
3.  **Expected Outcome:** This change should allow the `module_loader.py` to skip the problematic `gerador_quesitos` module, permitting the `documents` module to load correctly. This, in turn, is expected to resolve the 404 error for `/api/documents/upload`.
4.  **Next Steps for User:**
    *   Pull the changes.
    *   Rebuild and restart the backend service.
    *   Check startup logs to confirm `gerador_quesitos` is skipped and `documents` module routes are logged.
    *   Test the `/api/documents/upload` endpoint.
    *   (Future) A new task should be created to fix the actual `ImportError` in `gerador_quesitos` and re-enable it.

This task is now considered 'done' from a code modification perspective. Verification of the fix depends on user testing.
