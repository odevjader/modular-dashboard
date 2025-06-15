---
id: TASK-008
title: "FE Auth: Persistir Estado de Login Entre Recarregamentos de Página"
epic: "Bug Fix / Auth"
status: backlog
priority: high
dependencies: []
assignee: Jules
---

### Descrição

Atualmente, se um usuário autenticado recarregar a página no frontend, seu estado de login é perdido e ele é redirecionado para a página de login. É necessário investigar e corrigir o mecanismo de persistência e restauração da sessão do usuário para que ele permaneça logado entre recarregamentos.

### Critérios de Aceitação

- [ ] Usuário autenticado permanece logado após recarregar a página (F5 / Cmd+R).
- [ ] Token de autenticação (e possivelmente dados do usuário) é corretamente restaurado do `localStorage` ou similar ao iniciar a aplicação.
- [ ] `ProtectedRoute` e lógica de navegação respeitam o estado restaurado.

### Arquivos Relevantes

* `frontend/src/stores/authStore.ts`
* `frontend/src/App.tsx`
* `frontend/src/components/ProtectedRoute.tsx`
* `frontend/src/services/api.ts`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
