---
id: TASK-009
title: "Transcritor-PDF: Construir Orquestrador de Respostas com LLM"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-008"]
assignee: Jules
---

### Descrição

Criar `query_processor.py` em `transcritor-pdf` que usa a busca vetorial para obter contexto e um LLM para gerar respostas a perguntas sobre o documento.

### Critérios de Aceitação

- [ ] `src/query_processor.py` (ou similar) existe.
- [ ] Orquestrador recebe pergunta e ID do documento.
- [ ] Usa a inteligência de busca (TASK-016) para obter contexto.
- [ ] Constrói prompt e chama LLM (via `llm_client.py`).
- [ ] Retorna resposta do LLM.

### Arquivos Relevantes

* `transcritor-pdf/src/query_processor.py`
* `transcritor-pdf/src/extractor/llm_client.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
