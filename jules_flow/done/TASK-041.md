---
id: TASK-041
title: "DEV: Construir Interface de Chat no Frontend"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: done
priority: medium
dependencies: ["TASK-040"] # Depends on feedback processing (which implies doc is ready)
assignee: Jules
---

### Descrição

Interface de chat chamando `/api/documents/query/{document_id}`. (Original TASK-015 do backlog)

### Critérios de Aceitação

- [x] Interface de chat (área de mensagens, input de texto) implementada em AnalisadorDocumentosPage.tsx.
- [x] Lógica para enviar pergunta ao endpoint /api/documents/query/{document_id} e exibir resposta.

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`
* `frontend/src/services/api.ts`

### Relatório de Execução

**Frontend - Implementação da Interface e Lógica de Chat**

1.  **`frontend/src/services/api.ts`**:
    *   Definidas as interfaces `DocumentQueryPayload` (para o texto da pergunta) e `DocumentQueryResponse` (para a resposta da IA).
    *   Implementada a função assíncrona `postDocumentQuery(documentId: string, payload: DocumentQueryPayload)` que:
        *   Realiza uma requisição POST para o endpoint de gateway `/api/documents/query/{documentId}`.
        *   Envia o `query_text` no corpo da requisição.
        *   Inclui o token de autorização nos headers.
        *   Retorna a resposta da API contendo a resposta da IA.

2.  **`frontend/src/pages/AnalisadorDocumentosPage.tsx`**:
    *   **Integração com Zustand Store**: Importado `useAnalisadorStore` para acessar `processedDocumentId` (ID do documento processado) e `status` (status do processamento do documento, aqui chamado `docStatus`).
    *   **Gerenciamento de Estado do Chat**:
        *   `messages (Message[])`: Mantém o histórico das mensagens do chat (usuário e IA).
        *   `userInput (string)`: Controla o texto no campo de input.
        *   `isSending (boolean)`: Indica se uma mensagem está sendo enviada (para feedback visual e desabilitar controles).
    *   **Interface do Usuário (UI)**:
        *   Utilizados componentes MUI (`Paper`, `List`, `ListItem`, `TextField`, `Button`, `Tooltip`) para construir a interface.
        *   Área de mensagens rolável que renderiza as mensagens do array `messages`, diferenciando visualmente as mensagens do usuário e da IA.
        *   Campo de texto para o usuário digitar a pergunta, vinculado ao estado `userInput`.
        *   Botão "Enviar" para submeter a pergunta.
    *   **Lógica `handleSendMessage`**:
        *   Adiciona a mensagem do usuário à lista `messages` imediatamente.
        *   Limpa o campo de input.
        *   Define `isSending` para `true`.
        *   Chama `postDocumentQuery` com o `processedDocumentId` e `userInput`.
        *   Ao receber a resposta da API:
            *   Adiciona a resposta da IA à lista `messages`.
        *   Em caso de erro na API:
            *   Adiciona uma mensagem de erro genérica à lista `messages`.
            *   Loga o erro detalhado no console.
        *   Define `isSending` para `false` ao final da operação (sucesso ou erro).
    *   **Controle de Acesso ao Chat**:
        *   O campo de input e o botão "Enviar" são desabilitados se:
            *   `docStatus` não for `'success'`.
            *   `processedDocumentId` não estiver disponível.
            *   `isSending` for `true`.
        *   Um `Tooltip` no botão "Enviar" e um placeholder no `TextField` informam o usuário sobre a necessidade de um documento processado para habilitar o chat.

Com estas alterações, a interface de chat está funcional, permitindo ao usuário interagir com o documento processado através de perguntas e respostas.
