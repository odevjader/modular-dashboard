---
id: TASK-006
title: "Fix Celery ImportError in src/tasks.py"
epic: "Bugfix"
type: "development" # Tipos: development, research, test, documentation, review
status: backlog
priority: high
dependencies: []
assignee: Jules
---

### Descrição

Resolve an `ImportError: cannot import name 'app' from 'src.celery_app'` that occurs when the Celery worker starts. This prevents tasks from being processed.

### Critérios de Aceitação

- [ ] The Celery worker starts without the `ImportError`.
- [ ] Existing Celery tasks can be discovered and are operational.

### Arquivos Relevantes

* `src/tasks.py`
* `src/celery_app.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
