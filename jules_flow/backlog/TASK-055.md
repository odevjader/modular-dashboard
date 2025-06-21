---
id: TASK-055
title: "TEST-IMPL (Fase 2): Implementar Testes para `pdf_processor_service` e Novo Gateway"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: ["TASK-054"]
assignee: Jules
---

### Descrição

Implementar os testes unitários, de integração e E2E (conforme viável e se o framework estiver configurado) para o `pdf_processor_service` e o novo endpoint gateway, conforme definido no plano de teste da `TASK-054`.

### Critérios de Aceitação

- [ ] Testes unitários/integração para a lógica de extração de texto e DB no `pdf_processor_service` implementados.
- [ ] Testes de contrato/integração para o endpoint `/process-pdf` do `pdf_processor_service` implementados.
- [ ] Testes de contrato/integração para o endpoint gateway `/api/v1/documents/upload-and-process` implementados.
- [ ] Testes E2E (se aplicável) para o fluxo completo implementados.
- [ ] Todos os testes passando em ambiente de desenvolvimento/CI.

### Arquivos Relevantes

* `pdf_processor_service/tests/`
* `backend/tests/`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
