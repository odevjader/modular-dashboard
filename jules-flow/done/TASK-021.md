---
id: TASK-021
title: "TEST-PLAN: Planejar Testes para Endpoint `process-pdf` (Transcritor)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-020"]
assignee: Jules
---

### Descrição

Testes para `POST /process-pdf`: envio de PDF válido (verificar enfileiramento Celery), mock Celery/DB opcional.

### Critérios de Aceitação

- [ ] Plano de teste criado (e.g., `docs/tests/transcritor_process_pdf_test_plan.md`).
- [ ] Detalha cenários: PDF válido enfileira task, tratamento de erro para PDF inválido (se aplicável).

### Arquivos Relevantes

* `docs/tests/transcritor_process_pdf_test_plan.md`

### Relatório de Execução

- Analisado o comportamento do endpoint `POST /process-pdf` em `transcritor-pdf/src/main.py` e a lógica do pipeline em `transcritor-pdf/src/processing.py`.
- Definidos cenários de teste detalhados, cobrindo:
    - Upload de PDF válido e verificação do enfileiramento da tarefa Celery.
    - Upload de tipos de arquivo inválidos (e.g., `.txt`, `.jpg`).
    - Upload de PDF vazio (0 bytes).
    - Requisição sem arquivo.
    - Upload de PDF com nome de arquivo ausente (simulado).
    - Considerações para PDFs corrompidos e arquivos grandes.
- Estruturado o plano de teste com seções padrão: Introdução, Ambiente de Teste, Estratégia de Teste, Casos de Teste detalhados, Critérios de Sucesso e Itens Fora do Escopo.
- Criado o documento do plano de teste em `docs/tests/transcritor_process_pdf_test_plan.md` com base nos cenários e estrutura definidos.
- Ambos os critérios de aceitação foram atendidos.
