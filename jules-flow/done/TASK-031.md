---
id: TASK-031
title: "TEST-IMPL: Implementar Testes para Endpoint de Diálogo (Transcritor)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-030"]
assignee: Jules
---

### Descrição

Usar `TestClient` do FastAPI para o `transcritor-pdf` para testar o endpoint de diálogo.

### Critérios de Aceitação

- [ ] Testes de integração implementados em `transcritor-pdf/tests/test_api.py` (ou similar).
- [ ] Testes cobrem cenários de TASK-030, mockando o orquestrador.

### Arquivos Relevantes

* `transcritor-pdf/tests/test_api.py`

### Relatório de Execução

Testes de integração para o endpoint `POST /query-document/{document_id}` foram implementados em `transcritor-pdf/tests/test_api.py`. Foram utilizados `TestClient` do FastAPI e `unittest.mock.patch` com `AsyncMock` para simular o comportamento da função `get_llm_answer_with_context`. Os testes cobrem os cenários definidos em `TASK-030` (plano de teste `docs/tests/transcritor_query_dialog_test_plan.md`), incluindo:
    - `test_query_document_success`: Consulta bem-sucedida (200 OK).
    - `test_query_document_not_found_or_no_answer`: Contexto não encontrado ou sem resposta (404 Not Found).
    - `test_query_document_invalid_request_body`: Corpo da requisição inválido (422 Unprocessable Entity).
    - `test_query_document_orchestrator_error`: Erro no orquestrador mockado (500 Internal Server Error).
    As asserções verificam os códigos de status, o corpo das respostas e as chamadas aos mocks. Os testes foram escritos mas não puderam ser executados automaticamente devido a um erro no ambiente de execução de testes da ferramenta.
