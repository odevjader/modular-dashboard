---
id: TASK-032
title: "DEV: Expandir Gateway na API Principal para Diálogo"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-029", "TASK-014"] # Depends on transcritor dialog endpoint and API documents module
assignee: Jules
---

### Descrição

Rota `POST /api/documents/query/{document_id}` na API principal, chamando endpoint do `transcritor-pdf`. (Original TASK-011 do backlog)

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/query/{document_id}` implementada em `backend/app/modules/documents/router.py`.
- [ ] Rota requer autenticação.
- [ ] Aceita pergunta do usuário.
- [ ] `documents/services.py` chama `http://transcritor_pdf_service:8002/query-document/{document_id}`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
