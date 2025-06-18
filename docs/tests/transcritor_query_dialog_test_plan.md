# Test Plan: Endpoint de Diálogo (`/query-document/{document_id}`) - Transcritor PDF

**Document Version:** 1.0
**Date:** $(date +%Y-%m-%d)
**Author:** Jules (AI Agent)
**Task ID:** TASK-030

## 1. Introdução

Este plano de teste descreve a estratégia de teste para o endpoint de diálogo `POST /query-document/{document_id}` localizado em `transcritor-pdf/src/main.py`. Este endpoint permite que os usuários enviem uma pergunta para um documento específico e recebam uma resposta gerada por um LLM com base no contexto extraído do documento.

O foco principal destes testes é a integração do endpoint com o orquestrador de respostas (`get_llm_answer_with_context`), garantindo que as requisições sejam processadas corretamente e as respostas (ou erros) sejam formatadas como esperado.

## 2. Estratégia de Teste

Serão realizados testes de integração utilizando o `TestClient` do FastAPI. O componente principal a ser mockado é a função `get_llm_answer_with_context` (localizada em `src.query_processor`) para isolar o endpoint e controlar as respostas do orquestrador durante os testes.

## 3. Casos de Teste (Test Cases - TCs)

### TC_TDQ_001: Consulta bem-sucedida com `document_id` válido

*   **Descrição:** Testa o fluxo feliz onde um `document_id` válido e uma pergunta são fornecidos, e o orquestrador retorna uma resposta com sucesso.
*   **Pré-condições:** Nenhuma.
*   **Passos:**
    1.  Mockar `src.main.get_llm_answer_with_context` para retornar um dicionário de sucesso (e.g., `{"answer": "Esta é a resposta.", "retrieved_context": [{"text_content": "contexto"}], "error": None}`).
    2.  Enviar uma requisição `POST` para `/query-document/doc_valido_123` com o corpo JSON `{"user_query": "Qual é o tópico?"}`.
*   **Dados de Teste:**
    *   `document_id`: "doc_valido_123"
    *   Request body: `{"user_query": "Qual é o tópico?"}`
    *   Mocked response: `{"answer": "Esta é a resposta.", "retrieved_context": [{"text_content": "contexto"}], "error": None}`
*   **Resultado Esperado:**
    *   Código de status HTTP: 200 OK.
    *   Corpo da resposta JSON: Deve ser idêntico ao `Mocked response` acima.

### TC_TDQ_002: Consulta para `document_id` não encontrado ou sem contexto

*   **Descrição:** Testa o cenário onde o orquestrador não encontra contexto para o `document_id` fornecido ou o `document_id` não é reconhecido pelo orquestrador.
*   **Pré-condições:** Nenhuma.
*   **Passos:**
    1.  Mockar `src.main.get_llm_answer_with_context` para retornar um dicionário indicando que nenhum contexto foi encontrado (e.g., `{"answer": "Não foi possível responder com base no documento.", "retrieved_context": [], "error": "No context found for document_id"}`).
    2.  Enviar uma requisição `POST` para `/query-document/doc_invalido_456` com o corpo JSON `{"user_query": "Detalhes específicos?"}`.
*   **Dados de Teste:**
    *   `document_id`: "doc_invalido_456"
    *   Request body: `{"user_query": "Detalhes específicos?"}`
    *   Mocked response: `{"answer": "Não foi possível responder com base no documento.", "retrieved_context": [], "error": "No context found for document_id"}`
*   **Resultado Esperado:**
    *   Código de status HTTP: 200 OK (assumindo que o endpoint ainda retorna 200 mas com a indicação de erro/sem resposta no corpo, conforme design atual do `get_llm_answer_with_context`).
    *   Corpo da resposta JSON: Deve ser idêntico ao `Mocked response`.

### TC_TDQ_003: Requisição com corpo inválido (e.g., `user_query` ausente)

*   **Descrição:** Testa a validação da requisição pelo FastAPI quando campos obrigatórios estão ausentes.
*   **Pré-condições:** Nenhuma.
*   **Passos:**
    1.  Enviar uma requisição `POST` para `/query-document/doc_qualquer_789` com um corpo JSON inválido (e.g., `{}`).
*   **Dados de Teste:**
    *   `document_id`: "doc_qualquer_789"
    *   Request body: `{}`
*   **Resultado Esperado:**
    *   Código de status HTTP: 422 Unprocessable Entity.
    *   Corpo da resposta JSON: Deve conter o erro de validação padrão do FastAPI indicando que `user_query` é obrigatório.

### TC_TDQ_004: Erro inesperado no orquestrador

*   **Descrição:** Testa o tratamento de erro do endpoint quando o `get_llm_answer_with_context` lança uma exceção inesperada.
*   **Pré-condições:** Nenhuma.
*   **Passos:**
    1.  Mockar `src.main.get_llm_answer_with_context` para levantar uma `Exception("Erro interno simulado")`.
    2.  Enviar uma requisição `POST` para `/query-document/doc_erro_101` com o corpo JSON `{"user_query": "Isso vai falhar?"}`.
*   **Dados de Teste:**
    *   `document_id`: "doc_erro_101"
    *   Request body: `{"user_query": "Isso vai falhar?"}`
*   **Resultado Esperado:**
    *   Código de status HTTP: 500 Internal Server Error.
    *   Corpo da resposta JSON: Deve conter uma mensagem de erro genérica (e.g., `{"detail":"Internal Server Error"}` ou similar, dependendo da configuração de exceções do FastAPI).
    *   _Nota: A implementação atual do endpoint em `main.py` pode não ter um `try-except` explícito em torno da chamada a `get_llm_answer_with_context`. O FastAPI geralmente lida com exceções não tratadas retornando um 500. O teste verificará esse comportamento padrão._

## 4. Estratégia de Mock

*   A função `get_llm_answer_with_context` em `transcritor-pdf/src/main.py` (ou mais precisamente, `src.main.get_llm_answer_with_context` se importado diretamente no namespace do módulo `main`) será mockada usando `unittest.mock.patch`.
*   Como `get_llm_answer_with_context` é uma função `async`, ela deve ser mockada com `unittest.mock.AsyncMock`.
*   O `return_value` do mock será configurado em cada caso de teste para simular diferentes cenários de resposta do orquestrador.

## 5. Configuração do Ambiente de Teste

*   Os testes serão implementados no arquivo `transcritor-pdf/tests/test_main_api.py` (ou um novo arquivo específico como `test_dialog_endpoint.py` se preferível).
*   Utilizar `from fastapi.testclient import TestClient`.
*   O `TestClient` será instanciado com a aplicação FastAPI (`app` de `src.main`).

## 6. Critérios de Passa/Falha

*   Um caso de teste passa se todos os resultados esperados (código de status HTTP e corpo da resposta) forem atendidos.
*   A suíte de testes passa se todos os casos de teste individuais passarem.
