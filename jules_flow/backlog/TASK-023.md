---
id: TASK-023
title: "DEV: Desenvolver Inteligência de Busca Vetorial (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-019", "TASK-020"] # Depende da doc do pgvector e do processamento de PDF que armazena os vetores
assignee: Jules
---

### Descrição

Em `transcritor-pdf/src/vectorizer/vector_store_handler.py`, implementar busca por similaridade em pgvector. (Original TASK-008 do backlog)

### Critérios de Aceitação

- [ ] Função em `vector_store_handler.py` aceita query e ID de documento.
- [ ] Conecta ao DB e executa query de similaridade vetorial (e.g., `<=>`) em `pgvector`.
- [ ] Retorna chunks de texto relevantes.

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/vector_store_handler.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
