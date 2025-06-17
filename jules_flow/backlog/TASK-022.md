---
id: TASK-022
title: "TEST-IMPL: Implementar Testes para Endpoint `process-pdf` (Transcritor)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-021"]
assignee: Jules
---

### Descrição

Usar `TestClient` do FastAPI para o `transcritor-pdf` para testar o endpoint `process-pdf`.

### Critérios de Aceitação

- [ ] Testes de integração implementados em `transcritor-pdf/tests/test_api.py` (ou similar).
- [ ] Testes cobrem cenários de TASK-021, mockando a execução da task Celery para focar no endpoint.

### Arquivos Relevantes

* `transcritor-pdf/tests/test_api.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
