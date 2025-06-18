# Frontend Analyzer - Development Summary & Patterns

Este documento resume as principais abordagens e padrões a serem utilizados no desenvolvimento do frontend para o módulo "Analisador de Documentos", com base na pesquisa da TASK-036.

## 1. Estrutura e Componentes React

*   **Organização de Componentes:**
    *   Componentes reutilizáveis (ex: botões, inputs, modais, cards de loading) devem residir em `frontend/src/components/common/`.
    *   Componentes específicos do módulo "Analisador de Documentos" (ex: `DocumentUploadForm`, `ChatInterface`, `ProcessingStatusIndicator`, `DocumentListItem`) devem ser criados dentro de `frontend/src/modules/analisador_documentos/components/`.
    *   A página principal do analisador será em `frontend/src/pages/AnalisadorDocumentosPage.tsx` (ou similar).
*   **Padrões de Componentes:**
    *   Utilizar componentes funcionais com Hooks.
    *   **Props:** Para passar dados e callbacks de componentes pais para filhos.
    *   **State Local (`useState`):** Para gerenciar o estado interno de componentes individuais (ex: valor de input de texto, visibilidade de um modal).
    *   **Efeitos (`useEffect`):** Para interações com o ciclo de vida do componente, como buscar dados iniciais (se aplicável localmente) ou configurar polling para status de processamento.
*   **Exemplo de Estrutura de Página (`AnalisadorDocumentosPage.tsx`):**
    ```tsx
    // Pseudocódigo
    // function AnalisadorDocumentosPage() {
    //   // Hooks do Zustand para estado global (veja seção Zustand)
    //   // State local para UI específica da página, se necessário

    //   return (
    //     <div>
    //       <h1>Analisador de Documentos</h1>
    //       <DocumentUploadForm />
    //       <ProcessingStatusIndicator />
    //       <DocumentList /> {/* Poderia ser parte do ChatInterface ou separado */}
    //       <ChatInterface />
    //     </div>
    //   );
    // }
    ```

## 2. Gerenciamento de Estado com Zustand

*   **Store Global:** Um store Zustand será usado para gerenciar o estado compartilhado do módulo Analisador de Documentos.
    *   Localização: `frontend/src/modules/analisador_documentos/stores/analisadorStore.ts` (ou similar).
*   **Estrutura do Estado (Exemplo Inicial):**
    ```typescript
    // interface AnalisadorState {
    //   uploadedFile: File | null;
    //   isUploading: boolean;
    //   uploadError: string | null;
    //   processingStatus: string | null; // ex: 'idle', 'processing', 'success', 'error'
    //   processingProgress: number; // 0-100
    //   currentDocumentId: string | null; // ID do documento ativo no chat
    //   chatMessages: Array<{ id: string, sender: 'user' | 'ai', text: string }>;
    //   // Futuramente: lista de documentos processados, etc.
    // }

    // interface AnalisadorActions {
    //   setUploadedFile: (file: File | null) => void;
    //   startUpload: () => Promise<void>; // Chamará o serviço da API
    //   setProcessingStatus: (status: string, progress?: number) => void;
    //   fetchProcessingStatus: (taskId: string) => Promise<void>; // Para polling
    //   sendMessageToChat: (message: string) => Promise<void>; // Chamará API de query
    //   addChatMessage: (message: { id: string, sender: 'user' | 'ai', text: string }) => void;
    //   // ... outras actions
    // }
    ```
*   **Criação do Store:**
    ```typescript
    // import { create } from 'zustand';
    // import { devtools, persist } from 'zustand/middleware'; // Opcional, mas útil

    // const useAnalisadorStore = create<AnalisadorState & AnalisadorActions>()(
    //   devtools(
    //     persist(
    //       (set, get) => ({
    //         // ... estado inicial e actions
    //         uploadedFile: null,
    //         isUploading: false,
    //         // ...
    //         startUpload: async () => { /* ... impl chamar api.ts ... */ },
    //         // ...
    //       }),
    //       { name: 'analisador-storage' } // Para persistência (localStorage/sessionStorage)
    //     )
    //   )
    // );
    ```
*   **Uso em Componentes:**
    ```tsx
    // const { uploadedFile, startUpload } = useAnalisadorStore();
    // const isUploading = useAnalisadorStore(state => state.isUploading);
    ```

## 3. Interação com API (Serviços em `frontend/src/services/api.ts`)

*   **Serviços Existentes:**
    *   O arquivo `frontend/src/services/api.ts` já contém um `apiClient` genérico para chamadas JSON (que lida com token Auth) e um exemplo de upload de arquivo (`postGerarQuesitos`) usando `fetch` e `FormData`.
*   **Novos Serviços para o Analisador:**
    *   **Upload de Documento para Análise:**
        *   Uma nova função em `api.ts`, similar a `postGerarQuesitos`, mas chamando o endpoint `POST /api/documents/upload` (criado na Fase 2/3, que encaminha para `transcritor-pdf`).
        *   Receberá `File` object, criará `FormData`.
        *   Retornará um ID de tarefa (`task_id`) para polling.
    *   **Polling de Status de Processamento:**
        *   Uma nova função em `api.ts` para chamar um endpoint de status (ex: `GET /api/documents/upload/status/{task_id}` - este endpoint precisa ser definido/verificado no backend).
        *   Será chamada repetidamente (com `setTimeout` no `useEffect` de um componente React ou na action do Zustand) até o processamento estar completo ou falhar.
    *   **Query de Documento (Chat):**
        *   Uma nova função em `api.ts` para chamar o endpoint `POST /api/documents/query/{document_id}` (criado na TASK-032).
        *   Enviará a pergunta do usuário e o `document_id`.
        *   Retornará a resposta da IA.
*   **Exemplo de Polling (dentro de uma action Zustand ou `useEffect`):**
    ```typescript
    // async function pollStatus(taskId, set, get) {
    //   try {
    //     const statusResponse = await api.getProcessingStatus(taskId); // Fictícia, precisa ser criada em api.ts
    //     set({ processingStatus: statusResponse.status, processingProgress: statusResponse.progress });
    //     if (statusResponse.status === 'processing' || statusResponse.status === 'pending') {
    //       setTimeout(() => pollStatus(taskId, set, get), 2000); // Poll a cada 2s
    //     } else if (statusResponse.status === 'success') {
    //       set({ currentDocumentId: statusResponse.documentId }); // Exemplo
    //     }
    //   } catch (error) {
    //     set({ processingStatus: 'error', uploadError: error.message });
    //   }
    // }
    ```
*   **Tratamento de Erros:**
    *   Seguir o padrão existente em `api.ts`: checar `response.ok` e tentar parsear JSON do erro.
    *   Propagar erros para o store Zustand para que a UI possa exibi-los.

## 4. Considerações Adicionais

*   **TypeScript:** Utilizar TypeScript em todo o desenvolvimento frontend para tipagem forte.
*   **Estilização:** Seguir o guia de estilo do frontend (`docs/frontend_style_guide.md`) e utilizar os componentes de UI existentes/padrões.
*   **Testes:** Planejar e implementar testes unitários e de integração para os componentes e stores (conforme guias do Zustand e React Testing Library).

Este resumo servirá como um guia inicial e pode ser expandido conforme o desenvolvimento avança.
