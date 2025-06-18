---
id: TASK-033
title: "TEST-PLAN: Planejar Testes para Gateway de Diálogo (API Principal)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-032"]
assignee: Jules
---

### Descrição

Testes de integração para `/api/documents/query/{document_id}`: mockar `transcritor-pdf`, verificar auth e formatação.

### Critérios de Aceitação

- [ ] Plano de teste criado (e.g., `docs/tests/api_gateway_dialog_test_plan.md`).
- [ ] Detalha cenários: chamada bem-sucedida (mockando `transcritor-pdf`), falha de autenticação.

### Arquivos Relevantes

* `docs/tests/api_gateway_dialog_test_plan.md`

### Relatório de Execução

O plano de teste para o endpoint de gateway de diálogo (`POST /api/documents/query/{document_id}`) foi criado e salvo em `docs/tests/api_gateway_dialog_test_plan.md`.
    O plano detalha:
    - Objetivos do teste e estratégia (mockando o serviço `transcritor-pdf`).
    - Ferramentas a serem utilizadas (Pytest, TestClient, mocks).
    - Casos de teste específicos cobrindo:
        - Autenticação e Autorização (sem token, token inválido).
        - Validação de Entrada (corpo JSON vazio, `user_query` vazia).
        - Proxy para o serviço `transcritor-pdf` (chamada bem-sucedida, erros 404 e 500 do serviço, falha de conexão, timeout).
    - Ambiente de teste e critérios de passa/falha.
    Os critérios de aceitação da tarefa foram atendidos.
