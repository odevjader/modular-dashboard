---
id: TASK-015
title: "Frontend: Construir Interface de Chat"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: backlog
priority: medium
dependencies: ["TASK-014", "TASK-011"] # Depende do processamento concluído e do endpoint de query da API
assignee: Jules
---

### Descrição

Na `AnalisadorDocumentosPage.tsx`, após processamento, exibir interface de chat para enviar perguntas e ver respostas sobre o documento.

### Critérios de Aceitação

- [ ] Interface de chat é exibida após conclusão do processamento.
- [ ] Contém área de exibição de conversa e input para perguntas.
- [ ] Ao enviar pergunta, chama `/api/documents/query/{document_id}`.

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
