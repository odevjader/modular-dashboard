# Test Plan: API Gateway Dialogue Endpoint

**Endpoint:** `POST /api/documents/query/{document_id}`
**Module:** `backend/app/modules/documents/router.py`
**Service Function:** `backend/app/modules/documents/services.py::handle_document_query`

## 1. Objetivos do Teste

Verificar a funcionalidade do endpoint de gateway de diálogo na API Principal, incluindo:
- Encaminhamento correto de requisições para o serviço `transcritor-pdf`.
- Tratamento adequado de respostas do serviço `transcritor-pdf`.
- Aplicação de autenticação.
- Tratamento de erros e cenários inválidos.

## 2. Estratégia de Teste

Testes de integração utilizando `fastapi.testclient.TestClient`. O serviço `transcritor-pdf` (chamado via `httpx` pela função `handle_document_query`) será mockado para isolar o teste ao gateway.

## 3. Ferramentas

- Pytest
- FastAPI TestClient
- `unittest.mock.patch` ou `pytest-mock` para mockar `httpx.AsyncClient.post` ou a função `services.handle_document_query`'s call to `httpx.AsyncClient.post`. Idealmente, mockar a chamada `httpx.AsyncClient.post` dentro de `services.handle_document_query` para testar a lógica do serviço do gateway também.

## 4. Casos de Teste

### 4.1. Autenticação e Autorização

| ID Teste  | Descrição                                      | Pré-condições                               | Passos                                                                                                | Dados de Entrada (corpo JSON)        | Mock `httpx.post` (retorno)                                      | Resultado Esperado                                                                                                |
| :-------- | :--------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------- | :----------------------------------- | :--------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| TC_AGD_001 | Requisição sem token de autenticação         | N/A                                         | 1. Enviar POST para `/api/documents/query/doc123` sem header `Authorization`.                         | `{"user_query": "teste"}`            | N/A (não deve ser chamado)                                       | Status Code: 401 Unauthorized. Resposta JSON contém `{"detail": "Not authenticated"}` (ou similar).            |
| TC_AGD_002 | Requisição com token de autenticação inválido | N/A                                         | 1. Enviar POST para `/api/documents/query/doc123` com header `Authorization: Bearer tokeninvalido`. | `{"user_query": "teste"}`            | N/A (não deve ser chamado)                                       | Status Code: 401 Unauthorized. Resposta JSON contém `{"detail": "Could not validate credentials"}` (ou similar). |

### 4.2. Validação de Entrada

| ID Teste  | Descrição                                  | Pré-condições                                  | Passos                                                                                                   | Dados de Entrada (corpo JSON)     | Mock `httpx.post` (retorno)          | Resultado Esperado                                                                                                   |
| :-------- | :----------------------------------------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------- | :-------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| TC_AGD_003 | Requisição com corpo JSON vazio            | Usuário autenticado                            | 1. Enviar POST para `/api/documents/query/doc123` com corpo `{}`.                                        | `{}`                              | N/A (não deve ser chamado)           | Status Code: 422 Unprocessable Entity. Resposta JSON detalha o erro de validação (e.g., `user_query` faltando). |
| TC_AGD_004 | Requisição com `user_query` vazio/nulo   | Usuário autenticado                            | 1. Enviar POST para `/api/documents/query/doc123` com corpo `{"user_query": ""}`.                      | `{"user_query": ""}`              | N/A (chamada para o serviço `handle_document_query` deve levantar HTTPException 400) | Status Code: 400 Bad Request. Resposta JSON `{"detail": "User query cannot be empty."}`.                          |

### 4.3. Proxy para Serviço `transcritor-pdf` (Mockado)

| ID Teste  | Descrição                                                               | Pré-condições                               | Passos                                                                                                                                    | Dados de Entrada (corpo JSON)     | Mock `httpx.post` (retorno para `http://transcritor_pdf_service:8002/query-document/doc123`) | Resultado Esperado                                                                                                                                                              |
| :-------- | :---------------------------------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TC_AGD_005 | Chamada bem-sucedida ao serviço `transcritor-pdf`                       | Usuário autenticado                         | 1. Configurar mock de `httpx.AsyncClient.post` para retornar status 200 e JSON `{"answer": "Resposta do transcritor"}`. <br> 2. Enviar POST. | `{"user_query": "Qual a resposta?"}` | `MagicMock(spec=httpx.Response, status_code=200, json=lambda: {"document_id": "doc123", "query": "Qual a resposta?", "answer": "Resposta do transcritor"})` | Status Code: 200 OK. Resposta JSON: `{"message": "Query successfully processed by transcriber.", "transcriber_data": {"document_id": "doc123", "query": "Qual a resposta?", "answer": "Resposta do transcritor"}, "original_document_id": "doc123", "queried_by_user_id": "<user_id>"}`. Mock chamado com URL e JSON corretos. |
| TC_AGD_006 | Serviço `transcritor-pdf` retorna erro 404 (e.g., documento não encontrado) | Usuário autenticado                         | 1. Configurar mock de `httpx.AsyncClient.post` para retornar status 404 e JSON `{"detail": "Document not found"}`. <br> 2. Enviar POST.      | `{"user_query": "Pergunta?"}`     | `MagicMock(spec=httpx.Response, status_code=404, json=lambda: {"detail": "Document not found"}, raise_for_status=...)` (mock `raise_for_status` para levantar `HTTPStatusError`) | Status Code: 404 Not Found (ou o status code que o gateway decidir retornar, e.g. 502 se ele não repassar o 404). Idealmente repassa o 404. Resposta JSON: `{"detail": "Error from transcriber query service: Status 404."}`. |
| TC_AGD_007 | Serviço `transcritor-pdf` retorna erro 500 (erro interno do transcritor) | Usuário autenticado                         | 1. Configurar mock de `httpx.AsyncClient.post` para retornar status 500 e JSON `{"detail": "Internal error"}`. <br> 2. Enviar POST.            | `{"user_query": "Pergunta?"}`     | `MagicMock(spec=httpx.Response, status_code=500, json=lambda: {"detail": "Internal error"}, raise_for_status=...)` | Status Code: 500 Internal Server Error (ou o status code que o gateway decidir retornar). Resposta JSON: `{"detail": "Error from transcriber query service: Status 500."}`. |
| TC_AGD_008 | Falha de conexão com serviço `transcritor-pdf` (e.g., `httpx.RequestError`) | Usuário autenticado                         | 1. Configurar mock de `httpx.AsyncClient.post` para levantar `httpx.RequestError("Connection failed")`. <br> 2. Enviar POST.                   | `{"user_query": "Pergunta?"}`     | Levantar `httpx.RequestError("Connection failed")`                                          | Status Code: 503 Service Unavailable. Resposta JSON: `{"detail": "Could not connect to transcriber query service."}`.                                                              |
| TC_AGD_009 | Timeout ao chamar serviço `transcritor-pdf`                             | Usuário autenticado                         | 1. Configurar mock de `httpx.AsyncClient.post` para levantar `httpx.TimeoutException("Timeout")`. <br> 2. Enviar POST.                           | `{"user_query": "Pergunta?"}`     | Levantar `httpx.TimeoutException("Timeout")`                                                | Status Code: 504 Gateway Timeout (ou 503 se o tratamento for genérico para `RequestError`). Resposta JSON: `{"detail": "Could not connect to transcriber query service."}` (assumindo que TimeoutException é pego pelo RequestError). |

## 5. Ambiente de Teste

- Python environment com todas as dependências do backend instaladas.
- Banco de dados de teste (pode não ser estritamente necessário se a autenticação for mockada ou usar tokens de teste válidos, e o serviço externo é mockado).

## 6. Critérios de Passa/Falha

- **Passa:** Todos os casos de teste executados retornam os resultados esperados (status codes, corpos de resposta, chamadas de mock corretas).
- **Falha:** Qualquer caso de teste que não retorna o resultado esperado.

## 7. Responsabilidades

- Implementação dos testes: Jules
- Revisão do plano e dos testes: Desenvolvedor
