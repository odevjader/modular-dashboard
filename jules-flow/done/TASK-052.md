---
id: TASK-052
title: "DEV (Fase 2): Atualizar Orquestração (docker-compose) para `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Adicionar o novo `pdf_processor_service` ao `docker-compose.yml` principal do projeto, configurando sua build, volumes, portas (se expostas internamente) e variáveis de ambiente necessárias para comunicação com o banco de dados e outros serviços.

### Critérios de Aceitação

- [x] Nova entrada de serviço para `pdf_processor_service` adicionada ao `docker-compose.yml`.
- [x] Configuração de `build` aponta para o `Dockerfile` do `pdf_processor_service`.
- [x] Variáveis de ambiente para conexão com o PostgreSQL (DB_HOST, DB_USER, etc.) configuradas (via `env_file` and explicit `DATABASE_URL` construction).
- [ ] Serviço é capaz de iniciar e se comunicar com o banco de dados dentro da rede Docker. (Configuration complete; actual test pending environment execution)
- [x] Considerar dependências de serviço (`depends_on`) se necessário. (depends_on `db` added)

### Arquivos Relevantes

* `docker-compose.yml`

### Relatório de Execução
### Relatório de Execução

O arquivo `docker-compose.yml` principal do projeto foi atualizado para incluir o novo `pdf_processor_service`.

1.  **Definição do Serviço `pdf_processor_service`**:
    *   Adicionada uma nova entrada de serviço denominada `pdf_processor_service`.
    *   **Build**: Configurado para usar o `Dockerfile` localizado em `backend/pdf_processor_service/` (context: `./backend/pdf_processor_service`, dockerfile: `Dockerfile`).
    *   **Nome do Container**: Definido como `pdf_processor_service`.
    *   **Variáveis de Ambiente**:
        *   `env_file`: Utiliza o arquivo comum `./backend/.env` para herdar variáveis como `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.
        *   `DATABASE_URL`: Explicitamente construída como `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` para garantir a conexão com o serviço de banco de dados `db`.
        *   `PYTHONPATH=/app`: Adicionado para garantir que os módulos internos do serviço sejam importáveis.
    *   **Volumes**: O código fonte do serviço (`./backend/pdf_processor_service`) é montado em `/app` dentro do container para permitir o desenvolvimento com live-reload (se o Uvicorn estiver configurado para isso no Dockerfile CMD, o que está).
    *   **Dependências**: Configurado `depends_on` para o serviço `db` com `condition: service_healthy`, garantindo que o banco de dados esteja pronto antes que o `pdf_processor_service` inicie.
    *   **Rede**: Conectado à rede `app-network`, permitindo a comunicação com outros serviços (como `db` e, potencialmente, o `api` principal).
    *   **Portas**: Nenhuma porta é exposta ao host por padrão, pois o serviço é planejado para ser acessado internamente (provavelmente pelo serviço `api`). O `Dockerfile` do serviço já expõe a porta 8000, que é usada pelo Uvicorn internamente no container.

A configuração no `docker-compose.yml` estabelece a orquestração do `pdf_processor_service`, permitindo que ele seja construído e executado como parte do ambiente Docker do projeto. A verificação final de comunicação com o banco de dados ocorreria ao executar `docker-compose up`.
