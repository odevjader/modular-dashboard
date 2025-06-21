---
id: TASK-050
title: "DEV (Fase 2): Implementar Lógica de Extração de Texto no `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Implementar a funcionalidade principal de extração de texto de arquivos PDF dentro do `pdf_processor_service`. Isso pode envolver o uso de bibliotecas como PyMuPDF, pdfminer.six, etc. O texto extraído deve ser dividido em chunks apropriados para armazenamento e futuro processamento/embedding.

### Critérios de Aceitação

- [ ] Função ou classe de serviço implementada para receber um caminho de arquivo PDF ou bytes de PDF.
- [ ] Lógica para abrir e ler o PDF implementada.
- [ ] Texto é extraído com sucesso de PDFs simples.
- [ ] Texto extraído é dividido em chunks de tamanho gerenciável (e.g., por parágrafos, ou contagem de tokens/palavras).
- [ ] Lógica para armazenar os chunks na tabela `pdf_processed_chunks` (criada na TASK-048) utilizando o `document_id` apropriado.

### Arquivos Relevantes

* `pdf_processor_service/app/services/extraction.py`
* `pdf_processor_service/app/db_interaction.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
