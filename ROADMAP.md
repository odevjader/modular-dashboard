# Roadmap - Modular Dashboard

Este documento descreve o roadmap de alto nível planejado para o desenvolvimento do Modular Dashboard como uma plataforma base versátil e extensível. É um guia direcional e está sujeito a alterações.

*(Última atualização: 22 de Abril de 2025, aprox. 00:36 -03)*

## Status Atual

O projeto está em **Desenvolvimento Ativo**. Para detalhes sobre o estado atual e bloqueios conhecidos, consulte a seção [Status Atual no README.md](./README.md#status-atual).

**Bloqueio Principal Atual:** Resolução do bug no endpoint de login (`/api/auth/v1/login`).

## Fases Planejadas

O desenvolvimento está organizado nas seguintes fases principais, com **foco inicial na construção do Core da Plataforma e do Mecanismo de Modularidade**:

### Fase 1: Fundação do Core, Correção, Refatoração Inicial e Docs Base (Em Andamento)

* **Objetivo:** Estabelecer o núcleo funcional mínimo da plataforma (Auth, User Mgmt), corrigir bloqueios críticos, definir a arquitetura de modularidade, remover dependências pesadas do Core inicial, e finalizar a documentação essencial.
* **Tarefas Principais:**
    * ✅ Estrutura básica do projeto (Frontend/Backend/Docker) definida.
    * ✅ Módulo exemplo `01_GERADOR_QUESITOS` V1 funcional implementado *(Nota: Dependências pesadas serão removidas nesta fase)*.
    * ✅ Configuração do Banco de Dados e Migrações (Alembic) funcionando para `users`.
    * ✅ Estrutura base do Backend para `Auth` e `User Management` implementada.
    * ✅ Documentação essencial inicial criada (README, Visão, Arquitetura, Setup, Estrutura, BD, Módulos iniciais, Fluxo, Roadmap, Onboarding).
    * 🚧 **Corrigir bug crítico no endpoint `/api/auth/v1/login` (Prioridade Máxima).**
    * ⬜ **Definir e Implementar Mecanismo de Modularidade Inicial (Backend/Frontend):** Decidir e implementar a abordagem para registrar/carregar módulos (API e UI).
    * ⬜ **Refatorar Container `api` para remover dependências pesadas de PDF/OCR (Docling, Tesseract):** (Prioridade Alta para agilizar builds/deploys do Core). *(Importante: Após esta etapa, o módulo `01_GERADOR_QUESITOS` ficará temporariamente inoperante ou parcialmente funcional até a Fase 2).*
    * ⬜ Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) após correção do bug.
    * ⬜ Integrar fluxo de autenticação (Login, Logout, Proteção de Rotas) e telas de Gerenciamento de Usuários no Frontend Core, considerando a arquitetura modular definida. *(Depende da correção do bug e da definição da modularidade UI)*.
    * ⬜ Solidificar e documentar as APIs do Core (Auth, User).
    * ⬜ Estabelecer padrões claros para desenvolvimento de novos módulos.

### Fase 2: Performance do Core e Reintegração de Processamento Pesado

* **Objetivo:** Otimizar o desempenho da plataforma base e reintegrar funcionalidades de processamento pesado (como PDF/OCR) de forma desacoplada através de um serviço dedicado.
* **Tarefas Planejadas:**
    * ⬜ **Investigar e Implementar Container Dedicado para Processamento de PDFs/OCR:** Criar e configurar o serviço/container separado para estas tarefas (ex: usando FastAPI ou outra ferramenta adequada). Definir sua API interna.
    * ⬜ **Refatorar módulo(s) dependentes (ex: `01_GERADOR_QUESITOS`)** para utilizarem o novo container de processamento dedicado (provavelmente via chamadas API internas ou uma fila de mensagens).
    * ⬜ **Otimizar performance geral do build e runtime Docker (Core):** Reduzir tempo de build, otimizar tamanho das imagens, analisar performance da API Core.
    * ⬜ Refinar tratamento de erros e logging no backend Core.

### Fase 3: Testes do Core, Segurança e Melhorias de UX Base

* **Objetivo:** Aumentar a confiabilidade e segurança do Core com testes, implementar segurança básica de API e refinar a experiência do usuário da plataforma base.
* **Tarefas Planejadas:**
    * ⬜ **Revisar, aprimorar e expandir cobertura de testes automatizados (Backend/Frontend), com foco principal no Core da plataforma.** *(Considerar testes existentes)*.
    * ⬜ Refinar a interface do usuário **base** (Shell, navegação principal, componentes compartilhados) com base no feedback inicial (melhorar feedback visual, tema claro/escuro).
    * ⬜ Implementar medidas de segurança na API Core (ex: rate limiting, análise de headers de segurança).
    * ⬜ Coletar feedback sobre a usabilidade e resultados do módulo exemplo `01_GERADOR_QUESITOS` *(após sua reativação na Fase 2)*.

### Fase 4: Expansão com Novos Módulos e Funcionalidades de Plataforma

* **Objetivo:** Começar a adicionar valor através de novos módulos e, em seguida, adicionar funcionalidades que suportem um ecossistema mais rico.
* **Tarefas Planejadas (Ordem Revisada):**
    * ⬜ **Desenvolver e integrar novos módulos de exemplo/aplicação** na plataforma (ex: Jurídico - Pesquisa Jurisprudência, Análise Médica; Outros Domínios - Vendas Dashboard, IoT Monitor). *(Prioridade após Core estável)*.
    * ⬜ Implementar funcionalidades de plataforma de suporte (ex: Sistema de Notificações internas/externas, Histórico de Atividades do usuário). *(Após novos módulos)*.
    * ⬜ Considerar/Implementar opções de escalabilidade e integrações (ex: Login com Google OAuth, Monitoramento com Sentry). *(Após novos módulos)*.
    * ⬜ Adicionar mais configurações e personalizações globais ou por módulo (via Painel Admin / Preferências Usuário).

---
*Legenda:*
* ✅ Concluído
* 🚧 Em Andamento / Bloqueado
* ⬜ Planejado / A Fazer
---

**Nota:** Este roadmap é um guia flexível. A ordem e o escopo das tarefas podem ser ajustados conforme o projeto avança e novas prioridades emergem.