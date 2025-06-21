---
id: TASK-052
title: "DEV (Fase 2): Atualizar Orquestração (docker-compose) para `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Adicionar o novo `pdf_processor_service` ao `docker-compose.yml` principal do projeto, configurando sua build, volumes, portas (se expostas internamente) e variáveis de ambiente necessárias para comunicação com o banco de dados e outros serviços.

### Critérios de Aceitação

- [ ] Nova entrada de serviço para `pdf_processor_service` adicionada ao `docker-compose.yml`.
- [ ] Configuração de `build` aponta para o `Dockerfile` do `pdf_processor_service`.
- [ ] Variáveis de ambiente para conexão com o PostgreSQL (DB_HOST, DB_USER, etc.) configuradas.
- [ ] Serviço é capaz de iniciar e se comunicar com o banco de dados dentro da rede Docker.
- [ ] Considerar dependências de serviço (`depends_on`) se necessário.

### Arquivos Relevantes

* `docker-compose.yml`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
