---
id: TASK-008
title: "Transcritor-PDF: Desenvolver Inteligência de Busca Vetorial"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-002"] # Assume que o transcritor já processa e armazena vetores
assignee: Jules
---

### Descrição

Implementar função em `transcritor-pdf` para buscar chunks de texto similares a uma query em um documento específico, usando pgvector.

### Critérios de Aceitação

- [ ] Função em `src/vectorizer/vector_store_handler.py` (ou similar) aceita query e document ID.
- [ ] Função consulta PostgreSQL/pgvector usando similaridade vetorial.
- [ ] Retorna os chunks de texto relevantes.

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/vector_store_handler.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
