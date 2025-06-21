---
id: TASK-053
title: "DEV (Fase 2): Implementar Endpoint Gateway `/api/v1/documents/upload-and-process` na API Principal"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Implementar um novo endpoint na API Principal (`backend`) que atuará como gateway para o `pdf_processor_service`. Este endpoint receberá um upload de arquivo PDF, o encaminhará para o `pdf_processor_service` (chamando o endpoint `POST /process-pdf` da TASK-051) e retornará a resposta ao cliente.

### Critérios de Aceitação

- [x] Nova rota `POST /api/v1/documents/upload-and-process` definida no módulo `documents` (ou um novo módulo apropriado) da API Principal.
- [x] Endpoint protegido por autenticação.
- [x] Endpoint aceita upload de arquivo PDF.
- [x] Endpoint faz uma requisição HTTP interna para o endpoint `POST /process-pdf` do `pdf_processor_service`, encaminhando o arquivo ou seus dados.
- [x] Endpoint retorna a resposta do `pdf_processor_service` ao cliente.
- [x] Tratamento de erros para falhas na comunicação com o `pdf_processor_service`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/core/config.py`

### Relatório de Execução
### Relatório de Execução

1.  **Configuração do Serviço de Destino**:
    *   Adicionada a variável `PDF_PROCESSOR_SERVICE_URL` (com default `http://pdf_processor_service:8000`) à classe `Settings` em `backend/app/core/config.py` para definir o endereço base do microserviço de processamento de PDF.

2.  **Implementação do Endpoint Gateway (`backend/app/modules/documents/router.py`)**:
    *   Criado um novo endpoint `POST /upload-and-process` no router existente em `backend/app/modules/documents/router.py` (prefixo `/documents`, resultando na rota `/api/v1/documents/upload-and-process` conforme o `API_PREFIX` global e o prefixo do router).
    *   **Autenticação**: O endpoint é protegido e requer um usuário ativo, utilizando a dependência `get_current_active_user`.
    *   **Upload de Arquivo**: Aceita um arquivo PDF através de `UploadFile`.
    *   **Validação de Tipo**: Verifica se o `content_type` do arquivo é `application/pdf`, retornando um erro 400 caso contrário.
    *   **Comunicação com Microserviço**:
        *   Utiliza `httpx.AsyncClient` para fazer uma requisição POST para o endpoint `/processing/process-pdf` do `pdf_processor_service` (URL construída a partir de `settings.PDF_PROCESSOR_SERVICE_URL`).
        *   O arquivo PDF (conteúdo e nome) é encaminhado na requisição para o microserviço.
        *   Um timeout de 30 segundos foi configurado para esta chamada interna.
    *   **Resposta**: Retorna diretamente a resposta JSON recebida do `pdf_processor_service` se a chamada for bem-sucedida.
    *   **Tratamento de Erros**:
        *   Captura `httpx.HTTPStatusError` para repassar erros específicos do microserviço (status code e detalhes) ao cliente.
        *   Captura `httpx.RequestError` para erros de comunicação/rede com o microserviço, retornando um status 503 (Service Unavailable).
        *   Inclui um `try-except Exception` genérico para outros erros inesperados durante o processo, retornando um status 500.

3.  **Registro do Router**:
    *   O router de documentos já estava registrado na aplicação principal FastAPI, conforme estabelecido em tarefas anteriores (TASK-014).

O endpoint gateway foi implementado com sucesso, permitindo que a API principal delegue o processamento de PDFs para o `pdf_processor_service` de forma segura e robusta.
