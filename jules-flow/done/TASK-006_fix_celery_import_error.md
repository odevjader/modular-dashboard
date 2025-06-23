---
id: TASK-006
title: "Fix Celery ImportError in src/tasks.py"
epic: "Bugfix"
type: "development" # Tipos: development, research, test, documentation, review
status: done
priority: high
dependencies: []
assignee: Jules
---

### Descrição

Resolve an `ImportError: cannot import name 'app' from 'src.celery_app'` that occurs when the Celery worker starts. This prevents tasks from being processed.

### Critérios de Aceitação

- [x] The Celery worker starts without the `ImportError`. (Verified by static analysis, fix directly addresses the cause)
- [ ] Existing Celery tasks can be discovered and are operational. (Requires runtime environment to fully verify)

### Arquivos Relevantes

* `transcritor-pdf/src/tasks.py`
* `transcritor-pdf/src/celery_app.py`

### Relatório de Execução

Modified `transcritor-pdf/src/tasks.py` to resolve the `ImportError`.
The issue was an attempt to import a non-existent `app` object from `transcritor-pdf/src/celery_app.py` at the end of the `tasks.py` file. The `celery_app.py` file correctly defines `celery_app`.

**Changes made:**
1. Removed the line `from .celery_app import app` in `transcritor-pdf/src/tasks.py`.
2. Changed the decorator for the `health_check_task` from `@app.task` to `@celery_app.task`, using the `celery_app` instance that is correctly imported at the top of the file (`from src.celery_app import celery_app`).

This change ensures that only the defined `celery_app` object is used for task decoration, resolving the import error. The first acceptance criterion is met based on this direct fix. The second criterion would require successful execution in the target environment.
