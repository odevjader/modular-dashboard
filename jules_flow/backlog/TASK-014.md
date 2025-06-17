---
id: TASK-014
title: "API: Implementar Endpoint de Upload no Módulo `documents`"
epic: "Fase 2: Implementação do Gateway de Comunicação na API Principal"
status: backlog
priority: medium
dependencies: ["TASK-013", "TASK-010"] # Depende do worker e API do transcritor estarem prontos para receber
assignee: Jules
---

### Descrição

Criar rota `POST /upload` no módulo `documents`, protegida por autenticação, que aceita `UploadFile` e usa um serviço para repassar o arquivo ao `transcritor-pdf`.

### Critérios de Aceitação

- [ ] Rota `POST /api/documents/upload` existe em `documents/router.py`.
- [ ] Rota requer autenticação (`get_current_active_user`).
- [ ] Aceita `UploadFile`.
- [ ] `documents/services.py` tem função para chamar `http://transcritor_pdf_service:8002/process-pdf` (ou endpoint similar do transcritor) com o arquivo.
- [ ] Respostas e erros do microserviço são gerenciados.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
