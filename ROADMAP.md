# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: 23 de Abril de 2025, aprox. 13:53 PM -03)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. O foco imediato é na configuração do processo de gestão e na simplificação temporária do frontend. A resolução de bloqueios técnicos anteriores (build Docker, login API) está temporariamente em espera.

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais:

### Fase 1: Setup do Processo e Simplificação Inicial (Em Andamento)

* **Objetivo:** Estabelecer as ferramentas e processos para gerenciamento de tarefas e contexto e organizar o estado inicial do frontend para facilitar o desenvolvimento do Core.
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Funcionalidade principal desativada)*.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * ✅ Documentação essencial inicial criada/atualizada (Visão, Arquitetura, Setup, Estrutura, BD, Módulos, Fluxo, Roadmap, Onboarding, Prompts).
    * ✅ Refatoração inicial do Container `api` (dependências não-core comentadas).
    * 🚧 **Remover temporariamente a tela/fluxo de login do Frontend:** Simplificar a UI inicial para permitir foco no desenvolvimento de outros componentes Core sem depender da autenticação funcional. *(Prioridade Imediata)*.
    * 🚧 **Implementar Modelo Híbrido de Gestão:** *(Prioridade Imediata)*.
        * Configurar GitHub Project Board (Kanban: Backlog, Planejado, Em Andamento, Revisão, Concluído).
        * Adotar GitHub Issues para rastreamento de todas as tarefas.
        * Criar pasta `.logs/task_summaries/` no repositório.
        * Integrar o passo de salvar o "Sumário Final para Orquestrador" como arquivo `.md` em `.logs/task_summaries/` ao fluxo de trabalho (requer atualização do `docs/07_...`).
        * Definir processo para vincular Issues, PRs e Sumários.
    * ⬜ Resolver erro de build Docker (`failed to fetch oauth token`). *(Após setup do processo)*.
    * ⬜ Corrigir bug crítico no endpoint `/api/auth/v1/login`. *(Após resolução do build)*.
    * ⬜ Definir e Implementar Mecanismo de Modularidade Inicial (Backend/Frontend).
    * ⬜ Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`). *(Após correção do login)*.
    * ⬜ Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core. *(Após Auth funcional)*.
    * ⬜ Solidificar e documentar as APIs do Core (Auth, User).
    * ⬜ Estabelecer padrões claros para desenvolvimento de novos módulos.

### Fase 2: Performance do Core e Reintegração de Processamento Pesado

* **Objetivo:** Otimizar o desempenho da plataforma base e reintegrar funcionalidades de processamento pesado (como PDF/OCR) de forma desacoplada através de um serviço dedicado.
* **Tarefas Planejadas:**
    * ⬜ Investigar e Implementar Container Dedicado para Processamento de PDFs/OCR.
    * ⬜ Refatorar módulo(s) dependentes (ex: `01_GERADOR_QUESITOS`) para utilizarem o novo container de processamento dedicado.
    * ⬜ Otimizar performance geral do build e runtime Docker (Core).
    * ⬜ Refinar tratamento de erros e logging no backend Core.

### Fase 3: Testes do Core, Segurança e Melhorias de UX Base

* **Objetivo:** Aumentar a confiabilidade e segurança do Core com testes, implementar segurança básica de API e refinar a experiência do usuário da plataforma base.
* **Tarefas Planejadas:**
    * ⬜ Revisar, aprimorar e expandir cobertura de testes automatizados (Backend/Frontend), com foco principal no Core da plataforma.
    * ⬜ Refinar a interface do usuário **base** (Shell, navegação principal, componentes compartilhados).
    * ⬜ Implementar medidas de segurança na API Core (ex: rate limiting, análise de headers de segurança).
    * ⬜ Coletar feedback sobre a usabilidade do módulo exemplo `01_GERADOR_QUESITOS` *(após sua reativação na Fase 2)*.

### Fase 4: Expansão com Novos Módulos e Funcionalidades de Plataforma

* **Objetivo:** Começar a adicionar valor através de novos módulos e, em seguida, adicionar funcionalidades que suportem um ecossistema mais rico.
* **Tarefas Planejadas:**
    * ⬜ Desenvolver e integrar novos módulos de exemplo/aplicação na plataforma.
    * ⬜ Implementar funcionalidades de plataforma de suporte (Notificações, Histórico).
    * ⬜ Considerar/Implementar opções de escalabilidade e integrações (OAuth, Sentry).
    * ⬜ Adicionar mais configurações/preferências (Painel Admin / User Prefs).

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado / Prioridade Atual
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem.