---
id: TASK-042
title: "DEV: Integrar ao Menu de Navegação Principal (Frontend)"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: done
priority: medium
dependencies: ["TASK-038"] # Depends on the page being created
assignee: Jules
---

### Descrição

Adicionar item de menu para a nova página 'Analisador de Documentos'. (Original TASK-016 do backlog)

### Critérios de Aceitação

- [x] Novo item de menu "Analisador de Documentos" adicionado ao `MainLayout.tsx` (ou similar).
- [x] Item de menu navega corretamente para a `AnalisadorDocumentosPage`.

### Arquivos Relevantes

* `frontend/src/layouts/MainLayout.tsx` (ou similar)

### Relatório de Execução

**Frontend - Integração do Analisador de Documentos ao Menu Principal**

1.  **`frontend/src/layouts/MainLayout.tsx`**:
    *   **Importação de Ícone**: Adicionado `import DescriptionIcon from '@mui/icons-material/Description';` para o ícone do novo item de menu.
    *   **Adição do Item de Menu**:
        *   Um novo componente `NavListItem` foi inserido na lista de navegação principal.
        *   Configurado com as seguintes propriedades:
            *   `to="/analisador-documentos"`: Aponta para a rota correta da página, conforme definido em `App.tsx`.
            *   `primary="Analisador de Documentos"`: Define o texto visível do item de menu.
            *   `icon={<DescriptionIcon />}`: Associa o ícone importado ao item.
            *   As propriedades `open`, `isSmallScreen`, e `onClick` (para fechar o drawer em telas pequenas) foram passadas adequadamente, mantendo o comportamento consistente com outros itens de menu.
        *   O item foi posicionado após o link "Home" e antes da seção de itens de menu gerados dinamicamente a partir do `moduleRegistry`, para uma organização lógica.

Com esta alteração, a página "Analisador de Documentos" está agora acessível diretamente através do menu de navegação principal, melhorando a usabilidade e integração do módulo no sistema.
