# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard. É um guia direcional e está sujeito a alterações com base nas prioridades, feedback e desafios encontrados.

*(Última atualização: Abril de 2025)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. Para detalhes sobre o estado atual e bloqueios conhecidos, consulte a seção [Status Atual no README.md](./README.md#status-atual).

**Bloqueio Principal Atual:** Resolução do bug no endpoint de login (`/api/auth/v1/login`).

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais:

### Fase 1: Fundação, Correção e Documentação Base (Em Andamento)

* **Objetivo:** Estabelecer a base funcional mínima, corrigir bloqueios críticos e criar a documentação essencial.
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo `gerador_quesitos` V1 funcional implementado.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * 🚧 **Corrigir bug crítico no endpoint `/api/auth/v1/login` (Prioridade Máxima).**
    * ⬜ Testar endpoints de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) após correção do bug.
    * ⬜ Integrar fluxo de autenticação (Login, Logout, Proteção de Rotas) e tela de Gerenciamento de Usuários no Frontend (`Login.tsx`, `AdminUsers.tsx`, Zustand store, services).
    * ⬜ Criar documentação essencial (README, Arquitetura, Setup Dev, Estrutura Pastas, Módulos Existentes, Fluxo de Trabalho).

### Fase 2: Otimização de Performance e Segurança Inicial

* **Objetivo:** Melhorar o desempenho de gargalos conhecidos e implementar medidas básicas de segurança.
* **Tarefas Planejadas:**
    * ⬜ Investigar e otimizar performance do processamento de PDF/OCR no módulo `gerador_quesitos` (possível uso de cache com Redis ou processamento assíncrono/background).
    * ⬜ Investigar e otimizar performance do build Docker (ex: multi-stage builds, `COMPOSE_BAKE=true`).
    * ⬜ Implementar medidas básicas de segurança na API (ex: rate limiting).
    * ⬜ Refinar tratamento de erros e logging no backend.

### Fase 3: Testes Automatizados e Melhorias de UX

* **Objetivo:** Aumentar a confiabilidade com testes e refinar a experiência do usuário.
* **Tarefas Planejadas:**
    * ⬜ Implementar suíte de testes automatizados para o backend (Pytest).
    * ⬜ Implementar testes básicos para o frontend (ex: Vitest, React Testing Library).
    * ⬜ Refinar a interface do usuário com base no feedback inicial (melhorar feedback visual, considerar tema escuro/claro).
    * ⬜ Coletar feedback sobre a usabilidade e resultados do módulo `gerador_quesitos`.

### Fase 4: Escalabilidade e Novas Funcionalidades

* **Objetivo:** Adicionar novos módulos, funcionalidades de plataforma e preparar para um maior número de usuários.
* **Tarefas Planejadas (Exemplos):**
    * ⬜ Desenvolver novos módulos de IA (ex: Pesquisa de Jurisprudência, Análise de Documentos Médicos, Gerador de Impugnação).
    * ⬜ Implementar funcionalidades de plataforma (ex: Sistema de Notificações, Histórico de Atividades detalhado).
    * ⬜ Considerar opções de escalabilidade de login (ex: Login com Google OAuth).
    * ⬜ Integrar monitoramento de erros e performance (ex: Sentry).
    * ⬜ Adicionar mais configurações e personalizações para os módulos.

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança.