---
id: TASK-013
title: "DEV: Implementar Endpoint de Upload no Módulo `documents`"
epic: "Fase 2: Implementação do Gateway de Comunicação na API Principal"
status: backlog
priority: medium
dependencies: ["TASK-010", "TASK-012"] # Depends on module structure and its tests
assignee: Jules
---

### Descrição

Rota `POST /upload` autenticada, aceitando `UploadFile`. Serviço para repassar o arquivo ao `transcritor-pdf` (endpoint `http://transcritor_pdf_service:8002/process-pdf`). (Original TASK-006 do backlog)

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/upload` implementada em `documents/router.py`.
- [ ] Rota usa `Depends(get_current_active_user)`.
- [ ] Aceita `UploadFile`.
- [ ] `documents/services.py` contém lógica para encaminhar o request para `http://transcritor_pdf_service:8002/process-pdf`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
