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
* ✅ **Pesquisa de Documentação (Docker, Redis, Celery):** Documentação oficial e melhores práticas pesquisadas (TASK-003).
* ✅ **Resumo de Documentação (Docker, Redis, Celery):** Sumários criados em `docs/reference/` (TASK-004).
* ✅ **Planejamento de Testes (Fase 1 Infra):** Plano de teste para a configuração da infraestrutura da Fase 1 criado (TASK-005).
* ✅ **Implementação de Testes (Fase 1 Infra):** Scripts de teste de integração para configuração da infraestrutura criados (TASK-006).
* ⚠️ **Execução de Testes (Fase 1 Infra):** BLOCKED - Pending manual execution due to environment limitations (TASK-007).

---

## Fase 1.5: Implementação do Sistema Jules-Flow ✅

**Épico:** Configurar o sistema de gerenciamento de tarefas Jules-Flow.
*Objetivo: Estabelecer a estrutura e os processos para que Jules (AI Agent) possa gerenciar suas próprias tarefas de desenvolvimento de forma organizada e rastreável.*

* ✅ **Criação da Estrutura Inicial do Jules-Flow:** Diretórios, arquivos base (`README.md`, `INSTRUCTIONS_FOR_JULES.md`, `TASK_INDEX.md`), e o template de tarefas (`task_template.md`) foram configurados.
* ✅ **Centralização de Documentos de Referência:** Documentos de referência do `transcritor-pdf` movidos para `docs/reference` (TASK-001).
* ✅ **Revisão de .env.example Pós-Fase 1:** Arquivos `.env.example` verificados e considerados adequados (TASK-002).
* ✅ **Definição do Processo de Criação de Tarefas On-Demand:** Documentação atualizada para permitir que o Desenvolvedor solicite tarefas diretamente, além daquelas geradas pelo Roadmap. (Referência: Commit de atualização de documentação do Jules-Flow)

---

## Fase 2: Infraestrutura de Microserviços 🎯

**Épico:** Construir a pipeline de extração de documentos como um microserviço, utilizando a API principal como um Gateway seguro.
*Objetivo: Criar a fundação de backend necessária para o processamento de PDFs de forma isolada e escalável.*

#### Tarefas Priorizadas:

* ✅ **DOC-SEARCH: Pesquisar Documentação (FastAPI)** (TASK-008)
* ✅ **DOC-SUMMARIZE: Resumir Documentação (FastAPI para Gateway)** (TASK-009)
* ✅ **DEV: Criar Módulo `documents` na API Principal** (TASK-010)
* ✅ **TEST-PLAN: Planejar Testes para Módulo `documents` (Estrutura)** (TASK-011)
* ✅ **TEST-IMPL: Implementar Testes para Módulo `documents` (Estrutura)** (TASK-012)
1. ✅ **DB Schema:** Definir e criar a migração (Alembic) para a nova tabela `pdf_processed_chunks` (TASK-048). (Script de migração criado; aplicação pendente de resolução de acesso ao BD no ambiente de execução)
2. ✅ **Orquestração:** Atualizar o `docker-compose.yml` para incluir o novo `pdf_processor_service` e garantir a comunicação entre os containers (TASK-052).
3. ✅ **Estrutura do Microserviço:** Criar a estrutura de pastas e arquivos (`Dockerfile`, `requirements.txt`, etc.) para o `pdf_processor_service` (TASK-049).
4. ✅ **Lógica do Microserviço:** Implementar a lógica de extração de texto e armazenamento no PostgreSQL dentro do `pdf_processor_service` (TASK-050).
5. ✅ **Endpoint do Microserviço:** Criar o endpoint `POST /process-pdf` no `pdf_processor_service`, que ficará acessível apenas dentro da rede do Docker (TASK-051).
6. ✅ **Endpoint Gateway na API Principal:** Implementar o endpoint `POST /api/v1/documents/upload-and-process` (TASK-053). Este endpoint será o único ponto de entrada público, responsável por:
   * Validar a autenticação e autorização do usuário.
   * Atuar como um proxy seguro, chamando o endpoint do microserviço.
   * ✅ Implementado endpoint `/api/documents/upload` (TASK-013) para upload e encaminhamento ao `transcritor_pdf_service`.
   * ✅ Criado plano de testes para o endpoint de upload `/api/documents/upload` (TASK-015).
   * ✅ Implementados testes de integração para `/api/documents/upload` (TASK-016, com ressalvas sobre execução ambiental).

---

## Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF) 📝

**Épico:** Habilitar a interação e diálogo com documentos através do backend do Transcritor-PDF.
*Objetivo: Desenvolver o backend do `transcritor-pdf` para suportar busca semântica e interação baseada em LLM com os textos extraídos. Esta fase foca na construção dos componentes de backend que permitem ao sistema 'entender' e responder perguntas sobre os documentos processados.*

* ✅ **DOC-SEARCH: Pesquisar Documentação (pgvector, LLM Client)** (TASK-018)
* ✅ **DOC-SUMMARIZE: Resumir Documentação (pgvector, LLM Client)** (TASK-019)
* ✅ **DEV: Implementar Endpoint de Processamento de PDF no Transcritor-PDF** (TASK-020)
* ✅ **TEST-PLAN: Planejar Testes para Endpoint \`process-pdf\` (Transcritor)** (TASK-021)
* ✅ **TEST-IMPL: Implementar Testes para Endpoint \`process-pdf\` (Transcritor)** (TASK-022)
* ✅ **DEV: Desenvolver Inteligência de Busca Vetorial (Transcritor-PDF)** (TASK-023)
* ✅ **TEST-PLAN: Planejar Testes para Busca Vetorial (Transcritor-PDF)** (TASK-024)
* ✅ **TEST-IMPL: Implementar Testes para Busca Vetorial (Transcritor-PDF)** (TASK-025)
* ✅ **DEV: Construir Orquestrador de Respostas com LLM (Transcritor-PDF)** (TASK-026)
* ✅ **TEST-PLAN: Planejar Testes para Orquestrador de Respostas (Transcritor-PDF)** (TASK-027)
* ✅ **TEST-IMPL: Implementar Testes para Orquestrador de Respostas (Transcritor-PDF)** (TASK-028)
* ✅ **DEV: Criar Endpoint de Diálogo no Transcritor-PDF** (TASK-029)
* ✅ **TEST-PLAN: Planejar Testes para Endpoint de Diálogo (Transcritor-PDF)** (TASK-030)
* ✅ **TEST-IMPL: Implementar Testes para Endpoint de Diálogo (Transcritor-PDF)** (TASK-031)
* ✅ **DEV: Expandir Gateway na API Principal para Diálogo** (TASK-032)
* ✅ **TEST-PLAN: Planejar Testes para Gateway de Diálogo (API Principal)** (TASK-033)
* ✅ **TEST-IMPL: Implementar Testes para Gateway de Diálogo (API Principal)** (TASK-034)
* ⚠️ **TEST-EXEC: Executar Testes da Fase 3 (Transcritor-PDF e Gateway Diálogo)** (TASK-035) - Bloqueado: Falha na execução automática de testes.

---

## Fase 4: Construção da Experiência do Usuário (Frontend) 📝

**Épico:** Desenvolver a interface do usuário para o novo módulo de análise e diálogo de documentos.
*Objetivo: Criar uma interface intuitiva no frontend que permita aos usuários fazer upload de documentos, visualizar o status do processamento, e interagir com os documentos processados através de um sistema de chat.*

* ✅ **DOC-SEARCH: Pesquisar Documentação (React, Zustand, Frontend API)** (TASK-036)
* ✅ **DOC-SUMMARIZE: Resumir Documentação (Frontend para Analisador)** (TASK-037)
* ✅ **DEV: Criar Página 'Analisador de Documentos' (Frontend)** (TASK-038)
* ✅ **DEV: Desenvolver Interface de Upload na Página (Frontend)** (TASK-039)
* ✅ **DEV: Implementar Feedback de Processamento no Frontend** (TASK-040)
* ✅ **DEV: Construir Interface de Chat no Frontend** (TASK-041)
* ✅ **DEV: Integrar ao Menu de Navegação Principal (Frontend)** (TASK-042)
* ✅ **TEST-PLAN: Planejar Testes para Frontend do Analisador de Documentos** (TASK-043)
* ✅ **TEST-IMPL: Implementar Testes para Frontend (Analisador)** (TASK-044) - Teste de componente inicial adicionado; execução da suíte completa pendente de investigação de timeouts.
* ⚠️ **TEST-EXEC: Executar Testes da Fase 4 (Frontend Analisador)** (TASK-045) - BLOQUEADO: TASK-044 pendente


---

## Fase 3: Melhorias do Frontend Core ✅

**Épico:** Aprimorar a usabilidade, consistência e performance da interface principal da aplicação.
*Objetivo: Refinar a experiência do usuário no 'core' da aplicação, estabelecendo uma base sólida para todos os módulos.*

#### Tarefas Sugeridas:

1.  ✅ **Implementar Notificações Globais (Toasts/Snackbars) no Core:** Implementar um mecanismo de notificação global (toasts/snackbars) no layout principal para dar feedback claro ao usuário sobre ações, erros ou informações importantes em pt-BR. Este sistema deverá ser utilizável por qualquer módulo.
2.  ✅ **Revisão da Responsividade e Layout do Core:** Realizar uma auditoria e otimizar o layout do `MainLayout` e componentes centrais (como navegação, cabeçalho, rodapé, se houver) para garantir uma experiência de usuário consistente e agradável em dispositivos móveis e tablets. Manter o idioma pt-BR.
3.  ✅ **Padronização de Componentes Visuais do Core:** Revisar os componentes visuais utilizados na interface principal (core) e criar/documentar um guia de estilo ou componentes reutilizáveis (ex: botões padrão, modais, cards) para garantir consistência visual. Todo o conteúdo em pt-BR.
4.  ✅ **Melhoria na Navegação Principal e Feedback Visual do Core:** Avaliar a usabilidade da navegação principal (menu lateral, cabeçalho) e implementar melhorias no feedback visual de interações (ex: estados de hover, active, focus) para tornar a experiência mais intuitiva. Manter o idioma pt-BR.
5.  ✅ **Otimização de Performance do Carregamento Inicial (Core):** Analisar e otimizar o tempo de carregamento inicial da aplicação principal, investigando o tamanho dos bundles, a estratégia de code splitting para o core e o carregamento de assets essenciais.

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

* ✅ **Notificações no Frontend:** Implementar um mecanismo de notificação global (toasts/snackbars) para dar feedback claro ao usuário. (Coberto pela Fase 3 Core)
* 📝 **Logging e Monitoramento:** Configurar um sistema de logging estruturado para todos os serviços e avaliar uma ferramenta de Application Performance Monitoring (APM).
* 📝 **Sistema de Alertas (Backend):** Configurar alertas proativos via e-mail para falhas críticas, notificando a equipe de desenvolvimento.

---

## Fase Final: Submissão 📝

**Épico:** Preparar a aplicação para a entrega final, garantindo que todos os componentes estejam revisados e a documentação atualizada.
*Objetivo: Realizar as últimas verificações e garantir que o projeto esteja em um estado polido e completo conforme o escopo definido.*

* ⚠️ **ENV-REVIEW: Revisão Final do .env.example (TASK-046) - BLOQUEADO: TASK-045 pendente**
* ⚠️ **SUBMIT: Entregar todas as alterações do Roadmap Completo (TASK-047) - BLOQUEADO: TASK-046 pendente**
