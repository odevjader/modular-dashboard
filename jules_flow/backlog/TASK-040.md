---
id: TASK-040
title: "DEV: Implementar Feedback de Processamento no Frontend"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: backlog
priority: medium
dependencies: ["TASK-039"]
assignee: Jules
---

### Descrição

Indicador de loading e polling/WebSocket para status. Requer endpoint `GET /api/documents/upload/{job_id}/status` na API. (Original TASK-014 do backlog)

### Critérios de Aceitação

- [ ] Interface exibe feedback visual (e.g., spinner, mensagem) durante o upload e processamento.
- [ ] Lógica de polling para `GET /api/documents/upload/{job_id}/status` implementada.
- [ ] *Adendo:* Rota `GET /api/documents/upload/{job_id}/status` definida e implementada na API Principal (`backend/app/modules/documents/router.py` e `services.py`). Este endpoint deve consultar o status da tarefa Celery (via ID do job retornado no upload).

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`
* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
