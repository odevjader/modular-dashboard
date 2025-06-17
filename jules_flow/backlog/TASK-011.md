---
id: TASK-011
title: "API: Expandir Gateway para Diálogo com Documentos"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-006", "TASK-010"]
assignee: Jules
---

### Descrição

Adicionar rota `POST /api/documents/query/{document_id}` na API principal, autenticada, que repassa a pergunta ao novo endpoint de diálogo do `transcritor-pdf`.

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/query/{document_id}` existe em `documents/router.py`.
- [ ] Requer autenticação.
- [ ] Aceita pergunta no corpo da requisição.
- [ ] `documents/services.py` tem função para chamar `http://transcritor_pdf_service:8002/query-document/{document_id}`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
