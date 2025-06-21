---
id: TASK-048
title: "DEV (Fase 2): Definir Schema e Migração para `pdf_processed_chunks`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Definir a estrutura da tabela `pdf_processed_chunks` no banco de dados PostgreSQL, que armazenará os chunks de texto extraídos dos PDFs processados pelo `pdf_processor_service`. Criar e aplicar uma migração Alembic para esta nova tabela.

### Critérios de Aceitação

- [ ] Modelo da tabela `pdf_processed_chunks` definido (e.g., em `backend/app/models/`).
- [ ] Campos incluem no mínimo: `id`, `document_id` (FK para uma futura tabela de documentos ou identificador único do documento original), `chunk_text`, `chunk_order`, `embedding` (opcional, pode ser outra tabela).
- [ ] Nova revisão Alembic criada para gerar a tabela `pdf_processed_chunks`.
- [ ] Migração Alembic aplicada com sucesso ao banco de dados.

### Arquivos Relevantes

* `backend/app/models/`
* `backend/alembic/versions/`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
