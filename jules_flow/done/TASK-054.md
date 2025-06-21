---
id: TASK-054
title: "TEST-PLAN (Fase 2): Planejar Testes para `pdf_processor_service` e Novo Gateway"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: ["TASK-053"]
assignee: Jules
---

### Descrição

Criar um plano de teste detalhado para o `pdf_processor_service` (abordando a extração de texto, armazenamento de chunks, e o endpoint `/process-pdf`) e para o novo endpoint gateway `/api/v1/documents/upload-and-process` na API Principal.

### Critérios de Aceitação

- [x] Plano de teste criado (e.g., em `docs/tests/pdf_processor_service_test_plan.md`).
- [x] Detalha testes unitários/integração para a lógica de extração de texto e interação com DB no `pdf_processor_service`.
- [x] Detalha testes de contrato/integração para o endpoint `/process-pdf` do `pdf_processor_service`.
- [x] Detalha testes de contrato/integração para o endpoint gateway `/api/v1/documents/upload-and-process`, incluindo autenticação e encaminhamento para o microserviço.
- [x] Esboça cenários para testes E2E (upload via gateway -> processamento no microserviço -> verificação de dados no DB).

### Arquivos Relevantes

* `docs/tests/pdf_processor_service_test_plan.md`

### Relatório de Execução
### Relatório de Execução

1.  **Criação do Plano de Teste**:
    *   Um novo documento de plano de teste foi criado em: `docs/tests/pdf_processing_pipeline_test_plan.md`.
    *   A data atual foi inserida no documento.

2.  **Conteúdo do Plano de Teste**:
    *   **Visão Geral**: Descreve o propósito e o escopo do plano de teste, cobrindo o `pdf_processor_service` e o endpoint gateway na API principal.
    *   **Escopo de Teste Detalhado**:
        *   **`pdf_processor_service` Unit Tests**: Especifica testes para `extraction_service.py` (hash, extração de texto, chunking) e `document_service.py` (criação de documentos/chunks, tratamento de duplicatas), além de modelos e core helpers.
        *   **`pdf_processor_service` Integration Tests**: Define casos de teste para o endpoint `POST /processing/process-pdf`, incluindo uploads válidos, duplicados, tipos de arquivo inválidos, arquivos vazios/corrompidos.
        *   **Main API Backend (Gateway) Integration Tests**: Especifica testes para o endpoint `POST /api/v1/documents/upload-and-process`, cobrindo upload bem-sucedido (com mock do microserviço), autenticação, tratamento de tipo de arquivo inválido no nível do gateway, encaminhamento de erros do microserviço e tratamento de erros de conexão com o microserviço.
    *   **Ambiente e Ferramentas de Teste**: Lista as ferramentas propostas (`pytest`, `pytest-mock`, `httpx`, `TestClient`, etc.) e considerações sobre o ambiente.
    *   **Requisitos de Dados de Teste**: Especifica a necessidade de vários tipos de arquivos PDF e não-PDF para teste.
    *   **Estratégia de Execução de Teste**: Define uma ordem para o desenvolvimento e execução dos testes.
    *   **Critérios de Sucesso**: Inclui aprovação em todos os testes e metas de cobertura de código.
    *   **Riscos e Mitigações**: Identifica riscos potenciais como configuração do ambiente de teste, variedade de PDFs e problemas de timeout, com sugestões de mitigação.

O plano de teste criado é abrangente e cobre todos os aspectos solicitados nos critérios de aceitação.
