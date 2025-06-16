---
id: TASK-008
title: "FE Auth: Persistir Estado de Login Entre Recarregamentos de Página"
epic: "Bug Fix / Auth"
status: done
priority: high
dependencies: []
assignee: Jules
completed_at: YYYY-MM-DD
---

### Descrição

Atualmente, se um usuário autenticado recarregar a página no frontend, seu estado de login é perdido e ele é redirecionado para a página de login. É necessário investigar e corrigir o mecanismo de persistência e restauração da sessão do usuário para que ele permaneça logado entre recarregamentos.

### Critérios de Aceitação

- [x] Usuário autenticado permanece logado após recarregar a página (F5 / Cmd+R).
- [x] Token de autenticação (e possivelmente dados do usuário) é corretamente restaurado do `localStorage` ou similar ao iniciar a aplicação.
- [x] `ProtectedRoute` e lógica de navegação respeitam o estado restaurado.

### Arquivos Relevantes
  - frontend/src/stores/authStore.ts
  - frontend/src/App.tsx
  - frontend/src/components/ProtectedRoute.tsx
  - frontend/src/services/api.ts

### Relatório de Execução

O bug que causava a perda do estado de login do usuário após o recarregamento da página foi investigado e corrigido.

**Análise da Causa Raiz:**
A investigação revelou que, embora o token de autenticação fosse carregado do `localStorage` ao iniciar a aplicação, o objeto `user` no `authStore` era sempre inicializado como `null` e não havia um processo para revalidar o token e buscar os dados do usuário. Consequentemente, o `ProtectedRoute` interpretava esse estado como "não autenticado" para rotas que exigiam verificação de roles e redirecionava prematuramente para a página de login.

**Modificações Implementadas:**

1.  **`frontend/src/services/api.ts`:**
    *   Verificado e garantido que o cliente API (`apiClient`) utiliza o token armazenado no `localStorage` para autenticar as requisições. Isso é crucial para que a chamada de `getCurrentUser` na inicialização seja bem-sucedida. A função `login` também foi confirmada por armazenar o token no `localStorage` após um login bem-sucedido.

2.  **`frontend/src/stores/authStore.ts`:**
    *   Adicionado um novo estado booleano `isLoading` ao store, inicializado como `true`.
    *   Implementada uma nova ação assíncrona `initializeAuth()`:
        *   Esta ação é responsável por verificar a existência de um token no estado inicial do store (que é carregado do `localStorage`).
        *   Se um token existe, `initializeAuth()` chama `apiGetCurrentUser(token)` para buscar os dados do usuário.
        *   Em caso de sucesso, o objeto `user` é atualizado no store e `isLoading` é definido como `false`.
        *   Em caso de falha (ex: token inválido/expirado), o token é removido do `localStorage` e do store, `user` é definido como `null`, e `isLoading` é definido como `false`.
        *   Se nenhum token for encontrado inicialmente, `isLoading` é simplesmente definido como `false`.
    *   As ações `login` e `logout` foram atualizadas para gerenciar o estado `isLoading` adequadamente.

3.  **`frontend/src/App.tsx`:**
    *   Um hook `useEffect` foi adicionado ao componente `App` para chamar a ação `initializeAuth()` uma vez quando a aplicação é montada.

4.  **`frontend/src/components/ProtectedRoute.tsx`:**
    *   O componente agora observa o estado `isLoading` do `authStore`.
    *   Enquanto `isLoading` for `true`, `ProtectedRoute` exibe um indicador de carregamento (`CircularProgress`), adiando qualquer decisão de redirecionamento.
    *   Somente após `isLoading` se tornar `false`, as verificações existentes de token e `user`/roles são executadas.

**Resultado Esperado:**
Com estas alterações, o estado de autenticação do usuário agora persiste corretamente entre recarregamentos de página. A aplicação espera a conclusão da tentativa de reidratação da sessão antes de proteger rotas ou redirecionar para o login, resultando na experiência de usuário esperada.
