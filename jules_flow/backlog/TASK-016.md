---
id: TASK-016
title: "TEST-IMPL: Implementar Testes para Endpoint de Upload"
epic: "Fase 2: Implementação do Gateway de Comunicação na API Principal"
status: backlog
priority: medium
dependencies: ["TASK-015"]
assignee: Jules
---

### Descrição

Usar `TestClient` do FastAPI para os testes de integração do endpoint de upload.

### Critérios de Aceitação

- [ ] Testes de integração implementados em `backend/tests/test_documents_module.py` (ou similar).
- [ ] Testes cobrem os cenários do plano (TASK-015) usando `TestClient`.
- [ ] Chamada ao `transcritor-pdf` é mockada para isolar o teste do gateway.

### Arquivos Relevantes

* `backend/tests/test_documents_module.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
