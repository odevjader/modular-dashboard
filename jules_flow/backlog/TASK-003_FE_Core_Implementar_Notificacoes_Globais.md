---
id: TASK-003
title: FE Core: Implementar Notificações Globais (Toasts/Snackbars)
epic: Melhorias do Frontend Core (Fase 3)
status: backlog
priority: medium
dependencies: []
assignee: Jules
complexity: medium
created_at: YYYY-MM-DD
completed_at:
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

* `caminho/para/arquivo1.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
