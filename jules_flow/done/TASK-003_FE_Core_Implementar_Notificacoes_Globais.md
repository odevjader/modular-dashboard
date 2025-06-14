---
id: TASK-003
title: FE Core: Implementar Notificações Globais (Toasts/Snackbars)
epic: Melhorias do Frontend Core (Fase 3)
status: done
priority: medium
dependencies: []
assignee: Jules
complexity: medium
created_at: YYYY-MM-DD
completed_at: YYYY-MM-DD
---

### Descrição

Implementar um mecanismo de notificação global (toasts/snackbars) no layout principal (`MainLayout.tsx`) para dar feedback claro ao usuário sobre ações (sucesso, erro, informação, aviso) em pt-BR. Este sistema deverá ser acionável a partir de qualquer parte da aplicação (ex: via um hook ou store Zustand) e ser visualmente consistente com o Material UI. Considerar acessibilidade (ex: ARIA roles).

### Critérios de Aceitação

- Um serviço/hook de notificação é criado e está acessível globalmente no frontend.
- É possível disparar notificações do tipo sucesso, erro, aviso e informação.
- As notificações aparecem de forma não obstrutiva (ex: canto superior direito ou inferior).
- As notificações desaparecem automaticamente após um tempo ou podem ser dispensadas pelo usuário.
- O estilo das notificações é consistente com o tema Material UI da aplicação.
- O sistema é implementado no `MainLayout.tsx` ou de forma que o contexto esteja disponível para ele.
- Demonstração de uso em um componente de exemplo ou em uma ação existente.
- Todo o texto das notificações padrão está em pt-BR.

### Arquivos Relevantes

* `frontend/src/stores/notificationStore.ts`
* `frontend/src/App.tsx`
* `frontend/src/components/Login.tsx`

### Relatório de Execução

O sistema de notificações globais (toasts/snackbars) foi implementado com sucesso.

**Resumo das Alterações:**

1.  **Biblioteca e Estado:**
    *   A biblioteca `notistack` foi instalada e configurada como provedora de notificações.
    *   Um store Zustand (`frontend/src/stores/notificationStore.ts`) foi criado para gerenciar o estado e as ações de notificação. Ele fornece funções auxiliares como `showSuccess`, `showError`, `showInfo`, e `showWarning` para disparar notificações.

2.  **Integração Global:**
    *   O `SnackbarProvider` do `notistack` foi integrado ao `frontend/src/App.tsx`, envolvendo a aplicação para garantir que as notificações estejam disponíveis globalmente.
    *   O provedor foi configurado para exibir até 5 notificações simultaneamente no canto superior direito, com desaparecimento automático após 3 segundos.
    *   Uma pequena componente `NotificationSetup` foi usada para conectar as funções do `notistack` (`enqueueSnackbar`, `closeSnackbar`) ao store Zustand.

3.  **Demonstração e Uso:**
    *   Para demonstrar a funcionalidade, notificações de sucesso e erro foram adicionadas ao componente `frontend/src/components/Login.tsx`. As mensagens são exibidas em pt-BR (ex: "Login bem-sucedido!", "Falha no login...").

4.  **Estilo e Acessibilidade:**
    *   A biblioteca `notistack` é projetada para ser compatível com Material UI, garantindo consistência visual com o tema da aplicação.
    *   As configurações padrão de acessibilidade (ARIA roles) do `notistack` foram mantidas.

5.  **Testes (via revisão de código):**
    *   Todos os tipos de notificação (`success`, `error`, `info`, `warning`) foram corretamente mapeados para as variantes do `notistack`.
    *   A configuração do `SnackbarProvider` (posicionamento, auto-hide) foi verificada.
    *   As mensagens em pt-BR no exemplo de login foram confirmadas.

O sistema de notificação está agora operacional e pode ser utilizado em toda a aplicação frontend para fornecer feedback aos usuários.

---
**Pós-Conclusão: Correção de Bug (Follow-up)**

Após a conclusão e commit inicial desta tarefa, um bug de runtime foi identificado no frontend:
`Uncaught SyntaxError: The requested module '/src/stores/authStore.ts' does not provide an export named 'AuthProvider' (at App.tsx:15:10)`

**Causa Raiz:**
Durante a integração do `SnackbarProvider` em `frontend/src/App.tsx`, um wrapper `<AuthProvider>` foi incorretamente adicionado. O `authStore.ts` é um store Zustand e não define nem exporta um componente `AuthProvider` no estilo React Context.

**Resolução:**
1.  O import de `AuthProvider` de `./stores/authStore` foi removido de `frontend/src/App.tsx`.
2.  As tags `<AuthProvider>` e `</AuthProvider>` que envolviam o `SnackbarProvider` e o `Router` em `frontend/src/App.tsx` foram removidas.
3.  A correção foi verificada, e o erro de runtime foi resolvido.
4.  Um commit subsequente (`Fix: Remove erroneous AuthProvider wrapper from App.tsx`) foi realizado para aplicar esta correção.

Esta nota serve para registrar a resolução completa de todos os impactos relacionados à implementação original da TASK-003.
