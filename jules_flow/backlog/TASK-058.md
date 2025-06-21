---
id: TASK-058
title: "DEV (Fase 4 Piloto): Refatorar Backend do `gerador_quesitos` para Usar Texto Pré-processado"
epic: "Fase 4: Módulo Piloto e Integração"
status: backlog
priority: medium
dependencies: ["TASK-050"]
assignee: Jules
---

### Descrição

Modificar o endpoint backend do módulo `gerador_quesitos` (`backend/app/modules/gerador_quesitos/`) para não processar mais o arquivo PDF diretamente. Em vez disso, deve receber um `document_id` (ou `file_hash`/`task_id` correspondente a um documento já processado pela pipeline de documentos) e buscar o texto pré-processado (e possivelmente chunks/embeddings) do banco de dados para então executar sua lógica de geração de quesitos com LangChain.

### Critérios de Aceitação

- [ ] Endpoint backend do `gerador_quesitos` modificado para aceitar um `document_id` (ou similar) em vez de um upload de arquivo direto.
- [ ] Lógica implementada para buscar texto/chunks processados do banco de dados (e.g., da tabela `pdf_processed_chunks` ou similar) usando o `document_id`.
- [ ] Lógica de geração de quesitos com LangChain adaptada para usar o texto recuperado do banco de dados.
- [ ] Endpoint retorna os quesitos gerados.

### Arquivos Relevantes

* `backend/app/modules/gerador_quesitos/router.py`
* `backend/app/modules/gerador_quesitos/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
