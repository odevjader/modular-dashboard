---
id: TASK-026
title: "DEV: Construir Orquestrador de Respostas com LLM (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-023", "TASK-019"] # Depende da busca vetorial e da doc do LLM client
assignee: Jules
---

### Descrição

Criar `src/query_processor.py` em `transcritor-pdf` usando busca vetorial e `llm_client.py`. (Original TASK-009 do backlog)

### Critérios de Aceitação

- [ ] Arquivo `transcritor-pdf/src/query_processor.py` criado.
- [ ] Classe/função que recebe pergunta e ID de documento.
- [ ] Utiliza a busca vetorial (TASK-023) para obter contexto.
- [ ] Constrói prompt para LLM e chama `llm_client.py`.
- [ ] Retorna resposta do LLM.

### Arquivos Relevantes

* `transcritor-pdf/src/query_processor.py`
* `transcritor-pdf/src/extractor/llm_client.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
