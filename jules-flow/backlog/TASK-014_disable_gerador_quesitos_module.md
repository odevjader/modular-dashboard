---
id: TASK-014
title: "Temporarily Disable Gerador Quesitos Module"
epic: "Bugfix - Backend Gateway Routing"
type: "config" # Or "workaround", "refactor"
status: backlog
priority: high
dependencies: ["TASK-013"] # Follows up on the diagnosis from TASK-013
assignee: Jules
---

### Descrição

The `gerador_quesitos` module currently has an `ImportError: cannot import name 'logger' from 'app.core.config'`, which prevents it and subsequent modules (like `documents`) from loading correctly. This leads to 404 errors for routes in those modules.

To unblock testing and development of the `documents` module, this task is to temporarily disable the `gerador_quesitos` module by setting `enabled: false` in `backend/app/config/modules.yaml`. A separate task should be created later to fix the import error in `gerador_quesitos` itself.

### Critérios de Aceitação

- [ ] The `gerador_quesitos` module entry in `backend/app/config/modules.yaml` is updated to `enabled: false`.
- [ ] The backend application starts without the `ImportError` previously caused by `gerador_quesitos`.
- [ ] The `documents` module and its routes (e.g., `/api/documents/upload`) are now successfully loaded and registered, as verifiable by startup logs.
- [ ] The 404 error on `/api/documents/upload` is resolved (assuming no other issues).

### Arquivos Relevantes

* `backend/app/config/modules.yaml` (to be modified)
* `backend/app/core/module_loader.py` (for understanding impact)
* Startup logs of the backend service (for verification)

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
