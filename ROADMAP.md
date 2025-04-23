# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: 23 de Abril de 2025, aprox. 12:05 PM -03)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. Para detalhes sobre o estado atual e bloqueios conhecidos, consulte a seção [Status Atual no README.md](./README.md#status-atual).

**Bloqueio Principal Atual:** Erro durante o build da imagem Docker da API (`failed to fetch oauth token`), impedindo a inicialização e validação.

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais, com **foco inicial na construção do Core da Plataforma e do Mecanismo de Modularidade**:

### Fase 1: Fundação do Core, Correção, Refatoração Inicial e Docs Base (Em Andamento)

* **Objetivo:** Estabelecer o núcleo funcional mínimo da plataforma, corrigir bloqueios críticos (Build e Login), definir a arquitetura de modularidade, remover dependências pesadas do Core inicial, e finalizar a documentação essencial.
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Funcionalidade principal desativada nesta fase)*.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * ✅ Documentação essencial inicial criada/atualizada (README, Visão, Arquitetura, Setup, Estrutura, BD, Módulos, Fluxo, Roadmap, Onboarding).
    * ✅ Refatorar Container `api` para remover dependências pesadas de PDF/OCR (Docling, Tesseract). *(Código comentado, validação final pendente após build)*.
    * 🚧 **Resolver erro de build Docker (`failed to fetch oauth token`) (Prioridade Máxima Atual).**
    * ⬜ Corrigir bug crítico no endpoint `/api/auth/v1/login`. *(Depende da resolução do build)*.
    * ⬜ Definir e Implementar Mecanismo de Modularidade Inicial (Backend/Frontend).
    * ⬜ Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`). *(Depende da correção do build e login)*.
    * ⬜ Integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core. *(Depende da correção do build e login)*.
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
    * ⬜ Revisar, aprimorar e expandir cobertura de testes automatizados (Backend/Frontend), com foco principal no Core da plataforma. *(Considerar testes existentes)*.
    * ⬜ Refinar a interface do usuário **base** (Shell, navegação principal, componentes compartilhados) com base no feedback inicial (melhorar feedback visual, tema claro/escuro).
    * ⬜ Implementar medidas de segurança na API Core (ex: rate limiting, análise de headers de segurança).
    * ⬜ Coletar feedback sobre a usabilidade do módulo exemplo `01_GERADOR_QUESITOS` *(após sua reativação na Fase 2)*.

### Fase 4: Expansão com Novos Módulos e Funcionalidades de Plataforma

* **Objetivo:** Começar a adicionar valor através de novos módulos e, em seguida, adicionar funcionalidades que suportem um ecossistema mais rico.
* **Tarefas Planejadas (Ordem Revisada):**
    * ⬜ Desenvolver e integrar novos módulos de exemplo/aplicação na plataforma. *(Prioridade após Core estável)*.
    * ⬜ Implementar funcionalidades de plataforma de suporte (Notificações, Histórico). *(Após novos módulos)*.
    * ⬜ Considerar/Implementar opções de escalabilidade e integrações (OAuth, Sentry). *(Após novos módulos)*.
    * ⬜ Adicionar mais configurações/preferências (Painel Admin / User Prefs).

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem.