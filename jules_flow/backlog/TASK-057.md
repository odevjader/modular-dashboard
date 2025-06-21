---
id: TASK-057
title: "DEV (Fase 4 Piloto): Refatorar Frontend do `gerador_quesitos` para Upload via Gateway"
epic: "Fase 4: Módulo Piloto e Integração"
status: backlog
priority: medium
dependencies: ["TASK-013"]
assignee: Jules
---

### Descrição

Modificar a interface do usuário do módulo `gerador_quesitos` para utilizar o novo fluxo de upload de documentos através do endpoint gateway da API Principal (presumivelmente `/api/documents/upload` ou o novo `/api/v1/documents/upload-and-process` se este for o relevante para o `gerador_quesitos`). O objetivo é alinhar este módulo com a arquitetura de processamento de documentos centralizada.

### Critérios de Aceitação

- [ ] Interface de upload de arquivo no `gerador_quesitos` (e.g., `frontend/src/modules/gerador_quesitos/`) modificada/implementada.
- [ ] Frontend chama o endpoint gateway apropriado para upload de documentos.
- [ ] Frontend lida com o `task_id` (ou `document_id`) retornado pelo gateway.
- [ ] A lógica subsequente no frontend do `gerador_quesitos` utiliza o `task_id`/`document_id` para interagir com o backend do módulo (que será refatorado na TASK-058).

### Arquivos Relevantes

* `frontend/src/modules/gerador_quesitos/`
* `frontend/src/services/api.ts`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
