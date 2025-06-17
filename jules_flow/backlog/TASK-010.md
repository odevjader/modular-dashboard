---
id: TASK-010
title: "Transcritor-PDF: Criar Endpoint de Diálogo"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-009"]
assignee: Jules
---

### Descrição

Definir rota `POST /query-document/{document_id}` no `transcritor-pdf/src/main.py` que usa o orquestrador de respostas.

### Critérios de Aceitação

- [ ] Rota `POST /query-document/{document_id}` existe em `transcritor-pdf/src/main.py`.
- [ ] Aceita pergunta em JSON.
- [ ] Chama o orquestrador de respostas (TASK-017).
- [ ] Retorna a resposta gerada.

### Arquivos Relevantes

* `transcritor-pdf/src/main.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
