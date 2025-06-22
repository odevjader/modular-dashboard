---
id: TASK-022
title: "TEST-IMPL: Implementar Testes para Endpoint `process-pdf` (Transcritor)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-021"]
assignee: Jules
---

### Descrição

Usar `TestClient` do FastAPI para o `transcritor-pdf` para testar o endpoint `process-pdf`.

### Critérios de Aceitação

- [ ] Testes de integração implementados em `transcritor-pdf/tests/test_api.py` (ou similar).
- [ ] Testes cobrem cenários de TASK-021, mockando a execução da task Celery para focar no endpoint.

### Arquivos Relevantes

* `transcritor-pdf/tests/test_api.py`

### Relatório de Execução

- Revisado o plano de teste de TASK-021 (`docs/tests/transcritor_process_pdf_test_plan.md`).
- Analisado o arquivo de teste existente `transcritor-pdf/tests/test_api.py`.
- Verificado que a maioria dos cenários de teste obrigatórios para o endpoint `/process-pdf` já estavam implementados, incluindo:
    - Teste de upload de PDF válido com mock da chamada Celery (`test_process_pdf_enqueues_task_and_returns_id`).
    - Teste para upload de tipo de arquivo incorreto (`test_process_pdf_wrong_file_type`).
    - Teste para upload de arquivo vazio (`test_process_pdf_empty_file_content`).
    - Teste para requisição sem arquivo (`test_process_pdf_no_file_provided`).
    - Teste para arquivo sem nome de arquivo (resultando em erro 422 da validação do FastAPI) (`test_process_pdf_no_filename`).
- Adicionado um novo caso de teste (`test_process_pdf_corrupted_file_read_error`) para cobrir o cenário TC_PDF_007, onde ocorre um erro durante a leitura do arquivo antes do enfileiramento da tarefa Celery. Este teste utiliza `MagicMock` para simular um `IOError` em `file.read()` e verifica se um erro HTTP 500 é retornado e a tarefa Celery não é chamada.
- Confirmado que os testes utilizam o `TestClient` do FastAPI e `unittest.mock` para mockar a chamada da tarefa Celery (`process_pdf_task.delay`), focando assim no comportamento do próprio endpoint.
- Os critérios de aceitação foram atendidos: os testes de integração estão em `transcritor-pdf/tests/test_api.py` e cobrem os cenários planejados em TASK-021, com o devido mock da tarefa Celery.
