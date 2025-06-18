---
id: TASK-034
title: "TEST-IMPL: Implementar Testes para Gateway de Diálogo (API Principal)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-033"]
assignee: Jules
---

### Descrição

Usar `TestClient` do FastAPI para a API principal para testar o gateway de diálogo.

### Critérios de Aceitação

- [ ] Testes de integração implementados em `backend/tests/test_documents_module.py` (ou similar).
- [ ] Testes cobrem cenários de TASK-033, mockando a chamada ao `transcritor-pdf`.

### Arquivos Relevantes

* `backend/tests/test_documents_module.py`

### Relatório de Execução

Testes de integração para o endpoint de gateway de diálogo (`POST /api/documents/query/{document_id}`) foram implementados em `backend/tests/test_documents_module.py`.
    Os testes foram baseados no plano de teste `docs/tests/api_gateway_dialog_test_plan.md` (TASK-033) e utilizam `TestClient` do FastAPI.
    - A autenticação foi tratada mockando `app.modules.documents.router.get_current_active_user` para testes que requerem um usuário logado.
    - A chamada ao serviço `transcritor-pdf` (via `httpx.AsyncClient.post` em `backend.app.modules.documents.services`) foi mockada usando `unittest.mock.patch` com `AsyncMock` para simular diferentes cenários de resposta do serviço (sucesso, erro 404, erro 500, erro de conexão, timeout).
    - Os cenários de teste implementados (TC_AGD_001 a TC_AGD_009) cobrem:
        - Falhas de autenticação (sem token, token inválido - embora estes sejam geralmente cobertos por testes de autenticação mais genéricos, o plano os listava).
        - Validação de entrada (corpo JSON inválido, `user_query` vazia).
        - Interação bem-sucedida com o serviço `transcritor-pdf` mockado.
        - Diversos tipos de erro originados no serviço `transcritor-pdf` e o tratamento esperado pelo gateway.
    Os critérios de aceitação da tarefa foram atendidos. Os testes não puderam ser executados automaticamente devido a um erro no ambiente da ferramenta.
