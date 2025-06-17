---
id: TASK-002
title: "Docker Compose: Criar Celery Worker para Transcritor-PDF"
epic: "Fase 1: Configuração da Infraestrutura e Integração Base"
status: backlog
priority: medium
dependencies: ["TASK-001"]
assignee: Jules
---

### Descrição

Adicionar um novo serviço `transcritor_pdf_worker` ao `docker-compose.yml`, configurar seu build, ambiente, comando para iniciar Celery, dependências (Redis, DB) e rede. Criar/configurar `celery_app.py` e `celeryconfig.py`.

### Critérios de Aceitação

- [ ] `docker-compose.yml` define o serviço `transcritor_pdf_worker`.
- [ ] Worker usa o mesmo contexto/Dockerfile do `transcritor_pdf` ou um específico.
- [ ] Variáveis de ambiente para Redis e DB estão configuradas.
- [ ] Comando inicia o Celery worker corretamente.
- [ ] Worker depende de `redis` e `db`.
- [ ] Worker está na `app-network`.
- [ ] `transcritor-pdf/src/celery_app.py` existe e está configurado com o broker Redis.
- [ ] `transcritor-pdf/src/celeryconfig.py` existe e está configurado.

### Arquivos Relevantes

* `docker-compose.yml`
* `transcritor-pdf/src/celery_app.py`
* `transcritor-pdf/src/celeryconfig.py`
* (possivelmente um novo `transcritor-pdf/Dockerfile.worker`)

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
