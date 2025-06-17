---
id: TASK-009
title: "Docker Compose: Adicionar Suporte a Filas de Tarefas (Redis)"
epic: "Fase 1: Configuração da Infraestrutura e Integração Base"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Modificar o arquivo `docker-compose.yml` para adicionar um novo serviço Redis, configurar persistência (opcional), expor a porta e definir dependências para outros serviços.

### Critérios de Aceitação

- [ ] `docker-compose.yml` inclui um serviço `redis` usando imagem oficial.
- [ ] Redis está configurado para persistência (se aplicável).
- [ ] Porta `6379` do Redis está exposta à `app-network`.
- [ ] Serviços `api` (se aplicável), `transcritor_pdf` e o futuro `transcritor_pdf_worker` declaram `depends_on: redis`.

### Arquivos Relevantes

* `docker-compose.yml`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
