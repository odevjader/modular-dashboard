# Roadmap Detalhado: Modular Dashboard

Este documento detalha o plano de desenvolvimento do projeto, com tarefas organizadas por fases e prioridades.

**Legenda de Status:**
* ✅ - Concluído
* 🎯 - Foco Atual / Em Andamento
* 📝 - A Fazer
* 🔭 - Visão Futura

---

## Fase 1: Fundação e MVP ✅

**Épico:** Construir a base sólida da aplicação.
*Esta fase representa o estado atual do projeto, com a arquitetura modular e funcionalidades essenciais já implementadas.*

* ✅ **Estrutura do Backend:** Implementada com FastAPI.
* ✅ **Estrutura do Frontend:** Desenvolvida com React, TypeScript e Vite.
* ✅ **Containerização:** Aplicação totalmente containerizada com Docker e Docker Compose.
* ✅ **Sistema de Modularidade:** Implementado no backend e frontend.
* ✅ **Módulo de Autenticação:** Módulo central (`core_module`) com autenticação via JWT.
* ✅ **Banco de Dados:** Configurado com PostgreSQL e Alembic.
* ✅ **Módulos de Exemplo:** Criados `gerador_quesitos`, `ai_test`, `info`.
* ✅ **Documentação Inicial:** Criada a documentação base do projeto.

---

## Fase 1.5: Implementação do Sistema Jules-Flow ✅

**Épico:** Configurar o sistema de gerenciamento de tarefas Jules-Flow.
*Objetivo: Estabelecer a estrutura e os processos para que Jules (AI Agent) possa gerenciar suas próprias tarefas de desenvolvimento de forma organizada e rastreável.*

* ✅ **Criação da Estrutura Inicial do Jules-Flow:** Diretórios, arquivos base (`README.md`, `INSTRUCTIONS_FOR_JULES.md`, `TASK_INDEX.md`), e o template de tarefas (`task_template.md`) foram configurados.
* 📝 **Definição do Processo de Criação de Tarefas On-Demand:** Documentação atualizada para permitir que o Desenvolvedor solicite tarefas diretamente, além daquelas geradas pelo Roadmap. (Referência: Commit de atualização de documentação do Jules-Flow)

---

## Fase 2: Infraestrutura de Microserviços 🎯

**Épico:** Construir a pipeline de extração de documentos como um microserviço, utilizando a API principal como um Gateway seguro.
*Objetivo: Criar a fundação de backend necessária para o processamento de PDFs de forma isolada e escalável.*

#### Tarefas Priorizadas:

1. 📝 **DB Schema:** Definir e criar a migração (Alembic) para a nova tabela `pdf_processed_chunks`.
2. 📝 **Orquestração:** Atualizar o `docker-compose.yml` para incluir o novo `pdf_processor_service` e garantir a comunicação entre os containers.
3. 📝 **Estrutura do Microserviço:** Criar a estrutura de pastas e arquivos (`Dockerfile`, `requirements.txt`, etc.) para o `pdf_processor_service`.
4. 📝 **Lógica do Microserviço:** Implementar a lógica de extração de texto e armazenamento no PostgreSQL dentro do `pdf_processor_service`.
5. 📝 **Endpoint do Microserviço:** Criar o endpoint `POST /process-pdf` no `worker`, que ficará acessível apenas dentro da rede do Docker.
6. 📝 **Endpoint Gateway na API Principal:** Implementar o endpoint `POST /api/v1/documents/upload-and-process`. Este endpoint será o único ponto de entrada público, responsável por:
   * Validar a autenticação e autorização do usuário.
   * Atuar como um proxy seguro, chamando o endpoint do microserviço.

---

## Fase 3: Melhorias do Frontend Core 📝

**Épico:** Aprimorar a usabilidade, consistência e performance da interface principal da aplicação.
*Objetivo: Refinar a experiência do usuário no 'core' da aplicação, estabelecendo uma base sólida para todos os módulos.*

#### Tarefas Sugeridas:

1.  **Implementar Notificações Globais (Toasts/Snackbars) no Core:** Implementar um mecanismo de notificação global (toasts/snackbars) no layout principal para dar feedback claro ao usuário sobre ações, erros ou informações importantes em pt-BR. Este sistema deverá ser utilizável por qualquer módulo.
2.  **Revisão da Responsividade e Layout do Core:** Realizar uma auditoria e otimizar o layout do `MainLayout` e componentes centrais (como navegação, cabeçalho, rodapé, se houver) para garantir uma experiência de usuário consistente e agradável em dispositivos móveis e tablets. Manter o idioma pt-BR.
3.  **Padronização de Componentes Visuais do Core:** Revisar os componentes visuais utilizados na interface principal (core) e criar/documentar um guia de estilo ou componentes reutilizáveis (ex: botões padrão, modais, cards) para garantir consistência visual. Todo o conteúdo em pt-BR.
4.  **Melhoria na Navegação Principal e Feedback Visual do Core:** Avaliar a usabilidade da navegação principal (menu lateral, cabeçalho) e implementar melhorias no feedback visual de interações (ex: estados de hover, active, focus) para tornar a experiência mais intuitiva. Manter o idioma pt-BR.
5.  **Otimização de Performance do Carregamento Inicial (Core):** Analisar e otimizar o tempo de carregamento inicial da aplicação principal, investigando o tamanho dos bundles, a estratégia de code splitting para o core e o carregamento de assets essenciais.

---

## Fase 4: Módulo Piloto e Integração 📝

**Épico:** Refatorar o `gerador_quesitos` para usar a nova arquitetura, servindo como modelo para futuros módulos.
*Objetivo: Validar o fluxo de ponta a ponta, desde o upload no frontend até a resposta da IA.*

* 📝 **Refatorar Frontend do Módulo:** Adicionar uma interface de upload de arquivo no módulo `gerador_quesitos` que chame o novo endpoint Gateway.
* 📝 **Refatorar Backend do Módulo:** Modificar o endpoint do `gerador_quesitos` para, em vez de processar o arquivo, usar o `file_hash` para buscar o texto pré-processado no banco de dados e então executar a lógica com LangChain.

---

## Fase 5: Governança e Maturidade 🔭

**Épico:** Amadurecer a plataforma, focando em usabilidade, monitoramento e segurança.
*Objetivo: Tornar a aplicação mais robusta e fácil de manter a longo prazo.*

* 📝 **Notificações no Frontend:** Implementar um mecanismo de notificação global (toasts/snackbars) para dar feedback claro ao usuário.
* 📝 **Logging e Monitoramento:** Configurar um sistema de logging estruturado para todos os serviços e avaliar uma ferramenta de Application Performance Monitoring (APM).
* 📝 **Sistema de Alertas (Backend):** Configurar alertas proativos via e-mail para falhas críticas, notificando a equipe de desenvolvimento.
