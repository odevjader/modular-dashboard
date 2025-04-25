#ROADMAP.md
# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: 25 de Abril de 2025 - Refletindo conclusão das Issues #9 e #17)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. O processo inicial de gestão de projetos foi configurado (Issues, Board) e o backlog inicial foi populado com as tarefas do roadmap. As refatorações da estrutura da API Core (Issues #9 e #17) foram concluídas, movendo `auth` e `health` para `core_modules`. O foco técnico imediato passa a ser a implementação do mecanismo de modularidade V1 (Issue #8). O fluxo de trabalho Humano-IA foi refinado e formalizado.

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais:

### Fase 1: Setup do Processo e Core Inicial (Em Andamento)

* **Objetivo:** Estabelecer as ferramentas e processos para gerenciamento de tarefas, refatorar a estrutura Core e implementar a modularidade base.
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Funcionalidade principal desativada)*.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * ✅ Documentação essencial inicial criada/atualizada.
    * ✅ Refatoração inicial do Container `api` (dependências não-core comentadas).
    * ✅ **Implementar Modelo Híbrido de Gestão:** (Issues #2 concluída - Board, Issues, Linking, Logs definidos e documentados).
    * ✅ Resolver erro de build Docker (`failed to fetch oauth token`). *(Verificado como resolvido)*.
    * ✅ **Refatorar Estrutura: Mover APIs Core (`auth`) para core_modules/ (Issue #9).** *(Concluído)*.
    * ✅ **Refatorar Estrutura: Mover APIs Core (`health`) para core_modules/ (Issue #17).** *(Concluído)*.
    * 🚧 **Implementar Mecanismo de Modularidade v1 (Backend/Frontend - Revisado) (Issue #8).** *(Prioridade Atual)*.
    * ⬜ Corrigir bug crítico no endpoint `/api/auth/v1/login` (#11). *(Depende de #8)*.
    * ⬜ **Remover temporariamente a tela/fluxo de login do Frontend (#12):** *(Status: "Em Andamento/Mantido")*.
    * ⬜ Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) (#13). *(Depende de #11)*.
    * ⬜ Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core (#14). *(Depende de #13)*.
    * ⬜ Solidificar e documentar as APIs do Core (Auth, User) (#15). *(Idealmente após #13)*.
    * ⬜ Estabelecer padrões claros para desenvolvimento de novos módulos (#16). *(Depende de #8)*.
    * *(Nota: Implementação de Templates de Issue/PR (#3, #4) e Milestones (#6) adiada - ver backlog de Issues)*.

### Fase 2: Performance do Core e Reintegração de Processamento Pesado
*(... restante do roadmap como estava ...)*
### Fase 3: Testes do Core, Segurança e Melhorias de UX Base
*(... restante do roadmap como estava ...)*
### Fase 4: Expansão com Novos Módulos e Funcionalidades de Plataforma
*(... restante do roadmap como estava ...)*

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado / Prioridade Atual
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem, gerenciadas via GitHub Issues e Project Board.