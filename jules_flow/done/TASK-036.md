---
id: TASK-036
title: "DOC-SEARCH: Pesquisar Documentação (React, Zustand, Frontend API)"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: done
priority: medium
dependencies: ["TASK-035"] # Fase 4 inicia após conclusão da Fase 3
assignee: Jules
---

### Descrição

Revisar/pesquisar documentação React, Zustand (se aplicável), e interação com API (upload, polling, chamadas via `frontend/src/services/api.ts`).

### Critérios de Aceitação

- [ ] URLs e informações chave sobre React (componentes, páginas), Zustand (estado global), e `fetch`/`axios` para chamadas de API (incluindo upload de FormData) coletadas.

### Arquivos Relevantes

* (Nenhum arquivo de código, pesquisa externa)

### Relatório de Execução

Pesquisa de documentação concluída para React, Zustand e interação com API no frontend.

    **Recursos Coletados:**

    **1. React:**
    - Documentação Principal: `https://react.dev/learn`
        - Foco: Componentes, Estado (useState), Props, Hooks (useEffect).
        - Seções específicas: 'Describing the UI', 'Adding Interactivity', 'Managing State'.
    - Referência da API: `https://react.dev/reference/react`

    **2. Zustand (State Management):**
    - Repositório GitHub (fonte primária e links para guias): `https://github.com/pmndrs/zustand`
    - Guias específicos dentro do repositório (`docs/guides/`):
        - `typescript.md` (para uso com TypeScript)
        - `slices-pattern.md` (para organizar o store)
        - `testing.md` (para testar stores Zustand)
        - `persisting-store-data.md` (para persistir o estado)
        - `updating-state.md#with-immer` (para atualizações imutáveis com Immer)
    - Conceitos chave: `create` para stores, uso como hook, actions com `set`, suporte async.

    **3. Interação com API no Frontend (via `fetch`):**
    - Análise de `frontend/src/services/api.ts`:
        - Utiliza `fetch` nativo, com wrapper `apiClient` para JSON e auth.
        - Upload de arquivos com `FormData` e `fetch` direto.
        - Autenticação via token JWT em `localStorage`.
        - Tratamento de erro com `response.ok` e `try...catch`.
    - MDN Fetch API: `https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch`
        - Confirma as práticas em `api.ts` (métodos, body, headers, erros).
    - MDN FormData: `https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects`
    - MDN Async/Await: `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function`
    - MDN Promises: `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises`
    - **Polling de Status**:
        - Não existe mecanismo genérico em `api.ts`.
        - Requer implementação customizada (e.g., `useEffect` com `setTimeout`/`setInterval` no React para chamar endpoints de status periodicamente).
        - Termos de pesquisa para padrões: 'React fetch polling', 'JavaScript polling with fetch'.

    A pesquisa forneceu os links e conceitos fundamentais para iniciar o desenvolvimento do frontend da Fase 4. Os critérios de aceitação foram atendidos.
