---
id: TASK-030
title: "TEST-PLAN: Planejar Testes para Endpoint de Diálogo (Transcritor)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-029"]
assignee: Jules
---

### Descrição

Testes de integração para `/query-document/{document_id}`: mockar orquestrador, verificar formatação da resposta.

### Critérios de Aceitação

- [x] Plano de teste criado (e.g., `docs/tests/transcritor_query_dialog_test_plan.md`).
- [x] Detalha como mockar o orquestrador ou seus componentes.
- [x] Especifica asserções para a resposta do endpoint.

### Arquivos Relevantes

* `docs/tests/transcritor_query_dialog_test_plan.md`

### Relatório de Execução

- Criado o plano de teste detalhado em `docs/tests/transcritor_query_dialog_test_plan.md`.
- O plano inclui:
    - Estratégia de teste de integração para o endpoint `/query-document/{document_id}`.
    - Quatro casos de teste (TC_TDQ_001 a TC_TDQ_004) cobrindo:
        - Consulta bem-sucedida.
        - Consulta para `document_id` não encontrado/sem contexto.
        - Requisição com corpo inválido.
        - Erro inesperado no orquestrador.
    - Detalhamento da estratégia de mock para `get_llm_answer_with_context` usando `unittest.mock.AsyncMock`.
    - Especificações para configuração do ambiente de teste com `TestClient`.
- Os critérios de aceitação foram atendidos com a criação deste plano.
