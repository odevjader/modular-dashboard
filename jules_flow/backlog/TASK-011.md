---
id: TASK-011
title: "Config: Ajustar Variáveis de Ambiente para API e Transcritor-PDF"
epic: "Fase 1: Configuração da Infraestrutura e Integração Base"
status: backlog
priority: medium
dependencies: ["TASK-009"]
assignee: Jules
---

### Descrição

Adicionar `REDIS_URL` e `DATABASE_URL` (se necessário) ao `.env.example`. Modificar `transcritor-pdf` e API principal para ler estas variáveis. Garantir que os serviços no Docker Compose as utilizem.

### Critérios de Aceitação

- [ ] `backend/.env.example` (ou similar) contém `REDIS_URL`.
- [ ] `transcritor-pdf/src/db_config.py` (ou similar) lê `DATABASE_URL` e `REDIS_URL` do ambiente.
- [ ] `backend/app/core/config.py` carrega `REDIS_URL` se necessário.
- [ ] Serviços `api`, `transcritor_pdf`, `transcritor_pdf_worker` no `docker-compose.yml` usam estas variáveis.

### Arquivos Relevantes

* `backend/.env.example`
* `transcritor-pdf/src/db_config.py` (ou similar)
* `backend/app/core/config.py`
* `docker-compose.yml`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
