---
id: TASK-013
title: "Frontend: Desenvolver Interface de Upload na Página"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: backlog
priority: medium
dependencies: ["TASK-012", "TASK-006", "TASK-007"] # Depende da página e do endpoint de upload da API
assignee: Jules
---

### Descrição

Adicionar formulário de upload de PDF na `AnalisadorDocumentosPage.tsx` que chama o endpoint `/api/documents/upload`.

### Critérios de Aceitação

- [ ] `AnalisadorDocumentosPage.tsx` tem formulário com input de arquivo PDF e botão de envio.
- [ ] Ao enviar, chama `api.ts` que faz POST para `/api/documents/upload`.

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`
* `frontend/src/services/api.ts`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
