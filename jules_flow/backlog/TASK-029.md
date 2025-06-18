---
id: TASK-029
title: "DEV: Criar Endpoint de Diálogo no Transcritor-PDF"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-026"] # Depende do orquestrador de respostas
assignee: Jules
---

### Descrição

Rota `POST /query-document/{document_id}` em `transcritor-pdf/src/main.py`. (Original TASK-010 do backlog)

### Critérios de Aceitação

- [ ] Rota `POST /query-document/{document_id}` implementada em `transcritor-pdf/src/main.py`.
- [ ] Aceita JSON com pergunta do usuário.
- [ ] Chama o orquestrador de respostas (TASK-026).
- [ ] Retorna a resposta gerada.

### Arquivos Relevantes

* `transcritor-pdf/src/main.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
