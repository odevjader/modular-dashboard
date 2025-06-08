#ROADMAP.md
# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: Novembro de 2025)*

## Status Atual

As APIs do Core (Auth, User) foram solidificadas e documentadas (OpenAPI) (#15). O foco técnico imediato passa a ser **Estabelecer padrões claros para desenvolvimento de novos módulos (#16)**.

## Fases Planejadas

### Fase 1: Setup do Processo e Core Inicial (Em Andamento)

* **Objetivo:** Estabelecer as ferramentas e processos para gerenciamento de tarefas, refatorar a estrutura Core e implementar a modularidade base.
* **Tarefas Principais:**
  * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
  * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Funcionalidade principal desativada)*.
  * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
  * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
  * ✅ Documentação essencial inicial criada/atualizada.
  * ✅ Refatoração inicial do Container `api` (dependências não-core comentadas).
  * ✅ **Implementar Modelo Híbrido de Gestão:** (Issue #2 concluída).
  * ✅ Resolver erro de build Docker (`failed to fetch oauth token`). *(Resolvido)*.
  * ✅ **Refatorar Estrutura: Mover APIs Core (`auth`, `health`) para core_modules/ (Issues #9, #17).** *(Concluído)*.
  * ✅ **Corrigir bug crítico no endpoint `/api/auth/v1/login` (#11).** *(Resolvido via configuração de ambiente)*.
  * ✅ **Implementar Mecanismo de Modularidade v1 (Issue #8).** *(Concluído)*.
    * **Backend:**
      * ✅ **Tarefa 1.1:** Criar o arquivo de configuração `modules.yaml` e os schemas de validação Pydantic.
      * ✅ **Tarefa 1.2:** Criar a função `load_modules` no novo arquivo `core/module_loader.py`.
      * ✅ **Tarefa 1.3:** Integrar o `load_modules` na inicialização da aplicação (`main.py`).
      * ✅ **Tarefa 1.4:** Limpar as importações estáticas do `api_router.py`.
    * **Frontend:**
      * ✅ **Tarefa 2.1:** Criar o registro de módulos do frontend (`moduleRegistry.ts`).
      * ✅ **Tarefa 2.2:** Implementar o roteamento dinâmico no `App.tsx` usando o registro.
      * ✅ **Tarefa 2.3:** Implementar a navegação dinâmica (barra lateral, página inicial) a partir do registro.
  * ✅ **Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) (#13).** *(Concluído)*.
  * ✅ Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core (#14). *(Concluído)*.
  * ✅ **Solidificar e documentar as APIs do Core (Auth, User) (#15).** *(Concluído)*.
  * 🚧 **Estabelecer padrões claros para desenvolvimento de novos módulos (#16).** *(Prioridade Atual)*.
  * *(Nota: Implementação de Templates de Issue/PR (#3, #4) e Milestones (#6) adiada - ver backlog de Issues)*.

### Fase 2: Performance do Core e Reintegração de Processamento Pesado

* **Objetivo:** Otimizar a performance do Core e reintegrar funcionalidades de processamento pesado de forma mais robusta e escalável.
* **Tarefas Principais:**
  * ⬜ **Criar Serviço Dedicado para PDF/OCR (Issue #7):** Mover a lógica de processamento de PDF/OCR do `01_GERADOR_QUESITOS` para um container/serviço worker separado (ex: Celery, ARQ) para evitar bloqueio da API principal.
  * ⬜ Reativar e refatorar o módulo `01_GERADOR_QUESITOS` para usar o novo serviço de processamento.
  * ⬜ Reativar e refatorar o módulo `03_AI_TEST` (se ainda for relevante) ou substituí-lo por uma suíte de health check de IA mais robusta.
  * ⬜ Implementar caching (Redis) para sessões de usuário e/ou resultados de queries frequentes.
  * ⬜ Otimizar queries de banco de dados e garantir uso correto de índices.

### Fase 3: Testes do Core, Segurança e Melhorias de UX Base

* **Objetivo:** Garantir a estabilidade e segurança da plataforma base e melhorar a experiência de uso geral.
* **Tarefas Principais:**
  * ⬜ Aumentar a cobertura de testes unitários e de integração para todo o Core (especialmente `core_modules`).
  * ⬜ Implementar testes e2e (end-to-end) para os fluxos críticos (login, navegação, acesso a módulos).
  * ⬜ Realizar uma revisão de segurança na autenticação, autorização e tratamento de inputs.
  * ⬜ Desenvolver um sistema de notificações/feedback para o usuário na interface (ex: toasts para sucesso/erro).
  * ⬜ Refinar o layout principal (`MainLayout.tsx`) e a responsividade para dispositivos móveis.
  * ⬜ Implementar um tema Dark/Light.

### Fase 4: Expansão com Novos Módulos e Funcionalidades de Plataforma

* **Objetivo:** Validar o mecanismo de modularidade criando novos módulos e adicionar funcionalidades que enriqueçam a plataforma como um todo.
* **Tarefas Principais:**
  * ⬜ Desenvolver um segundo módulo de exemplo completo para validar e refinar o processo de criação de módulos.
  * ⬜ Implementar um sistema de permissões mais granular (além de `USER`/`ADMIN`).
  * ⬜ Criar uma interface de administração para configurações globais da plataforma.
  * ⬜ Desenvolver um dashboard de métricas de uso da plataforma.
  * ⬜ Explorar a comunicação inter-módulos (se necessário).

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado / Prioridade Atual
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem, gerenciadas via GitHub Issues e Project Board.
