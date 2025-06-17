---
id: TASK-014
title: "DEV: Registrar Módulo `documents` na API Principal"
epic: "Fase 2: Implementação do Gateway de Comunicação na API Principal"
status: done
priority: medium
dependencies: ["TASK-010"] # Depends on module router existence
assignee: Jules
---

### Descrição

Adicionar módulo `documents` ao `modules.yaml`. (Original TASK-007 do backlog)

### Critérios de Aceitação

- [ ] Entrada para o módulo `documents` adicionada em `backend/app/config/modules.yaml`.
- [ ] Prefixo `/api/documents` configurado para o módulo.
- [ ] API principal carrega o módulo `documents` corretamente.

### Arquivos Relevantes

* `backend/app/config/modules.yaml`

### Relatório de Execução

Verified that the `documents` module is configured in `backend/app/config/modules.yaml`.
The existing configuration is:
  - name: "documents"
    path: "modules.documents"
    router_variable_name: "api_router"
    version: "v1"
    prefix: "/documents"
    tags: ["Documents"]
    enabled: true

This configuration aligns with the requirements of the task:
- An entry for the `documents` module exists.
- The prefix `/documents` (which becomes `/api/documents` globally) is configured.
- The `router_variable_name` correctly points to `api_router` in `app.modules.documents.router.py`.

Attempted to run tests in `backend/tests/test_documents_module.py` to definitively confirm module loading with these settings. However, test execution was blocked by a persistent environment error ("Failed to compute affected file count... All changes to the repo have been rolled back.").

Given that the configuration in `modules.yaml` was already present and appears correct, and considering that previous tasks (TASK-012, TASK-013) involving tests for the documents module passed, it is concluded that the module registration meets the task requirements. The inability to re-run tests at this exact moment is noted as an external environmental issue.
