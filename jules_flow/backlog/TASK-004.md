---
id: TASK-004
title: "Docker Compose: Corrigir Dependências e Conectividade"
epic: "Fase 1: Configuração da Infraestrutura e Integração Base"
status: backlog
priority: medium
dependencies: ["TASK-002", "TASK-003"]
assignee: Jules
---

### Descrição

Revisar `docker-compose.yml` para garantir que `api`, `transcritor_pdf`, e `transcritor_pdf_worker` tenham as corretas `depends_on` declarações para `redis` e `db`. Verificar `PYTHONPATH` para os serviços do transcritor.

### Critérios de Aceitação

- [ ] `api` depende de `redis` (se aplicável) no `docker-compose.yml`.
- [ ] `transcritor_pdf` depende de `redis` e `db` no `docker-compose.yml`.
- [ ] `transcritor_pdf_worker` depende de `redis` e `db` no `docker-compose.yml`.
- [ ] `PYTHONPATH` está corretamente configurado para `transcritor-pdf` e `transcritor_pdf_worker`.

### Arquivos Relevantes

* `docker-compose.yml`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
