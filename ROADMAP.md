#ROADMAP.md
# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: 24 de Abril de 2025)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. O processo inicial de gestão de projetos foi configurado (Issues, Board) e o backlog inicial foi populado com as tarefas do roadmap. O foco técnico imediato está na refatoração da estrutura de pastas da API Core (Issue #9), seguido pela implementação do mecanismo de modularidade V1 (Issue #8).

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais:

### Fase 1: Setup do Processo e Core Inicial (Em Andamento)

* **Objetivo:** Estabelecer as ferramentas e processos para gerenciamento de tarefas, simplificar o frontend inicial e resolver bloqueios técnicos chave para habilitar o desenvolvimento do Core (Auth/User).
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Funcionalidade principal desativada)*.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * ✅ Documentação essencial inicial criada/atualizada (Visão, Arquitetura, Setup, Estrutura, BD, Módulos, Fluxo, Roadmap, Onboarding, Prompts, Gestão).
    * ✅ Refatoração inicial do Container `api` (dependências não-core comentadas).
    * ✅ **Implementar Modelo Híbrido de Gestão:** (Issues #2 concluída - Board, Issues, Linking, Logs definidos e documentados).
    * ✅ Resolver erro de build Docker (`failed to fetch oauth token`). *(Nota: Resolvido conforme handoff, pendente de verificação final no próximo build)*.
    * 🚧 **Refatorar Estrutura: Mover APIs Core para core_modules/ (Issue #9).** *(Prioridade Atual)*.
    * ⬜ Implementar Mecanismo de Modularidade v1 (Backend/Frontend - Revisado) (Issue #8). *(Depende de #9)*.
    * ⬜ Corrigir bug crítico no endpoint `/api/auth/v1/login` (#11). *(Após Modularidade V1)*.
    * ⬜ **Remover temporariamente a tela/fluxo de login do Frontend (#12):** *(Em Andamento/Mantido)*.
    * ⬜ Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) (#13). *(Depende de #11)*.
    * ⬜ Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core (#14). *(Depende de #13)*.
    * ⬜ Solidificar e documentar as APIs do Core (Auth, User) (#15).
    * ⬜ Estabelecer padrões claros para desenvolvimento de novos módulos (#16). *(Depende de #8)*.
    * *(Nota: Implementação de Templates de Issue/PR (#3, #4) e Milestones (#6) adiada - ver backlog de Issues)*.

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

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem, gerenciadas via GitHub Issues e Project Board.