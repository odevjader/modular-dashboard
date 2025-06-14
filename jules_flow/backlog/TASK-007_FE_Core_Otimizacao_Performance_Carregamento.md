---
id: TASK-007
title: FE Core: Otimização de Performance do Carregamento Inicial
epic: Melhorias do Frontend Core (Fase 3)
status: backlog
priority: medium
dependencies: []
assignee: Jules
complexity: high
created_at: YYYY-MM-DD
completed_at:
---

### Descrição

Analisar o tempo de carregamento inicial da aplicação principal (bundle do frontend). Investigar o tamanho dos bundles (usando `vite-bundle-visualizer` ou similar), a estratégia de code splitting para o core (rotas e componentes no `App.tsx` e `MainLayout.tsx`), e o carregamento de assets essenciais. Implementar otimizações para reduzir o tempo de carregamento inicial.

### Critérios de Aceitação

- Uma análise do bundle do frontend é realizada e os resultados são resumidos na tarefa (ou em um arquivo anexo).
- Pelo menos 2-3 otimizações são identificadas e implementadas. Exemplos:
    - Lazy loading de componentes/rotas que não são imediatamente necessários.
    - Otimização de imagens ou outros assets pesados carregados inicialmente.
    - Revisão de dependências grandes que podem ser substituídas ou removidas.
- Uma medição (antes e depois, usando Lighthouse ou DevTools) mostra uma melhoria perceptível no tempo de carregamento ou no score de performance.

### Arquivos Relevantes

* `caminho/para/arquivo1.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
