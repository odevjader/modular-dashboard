---
id: TASK-039
title: "DEV: Desenvolver Interface de Upload na Página (Frontend)"
epic: "Fase 4: Construção da Experiência do Usuário (Frontend)"
status: done
priority: medium
dependencies: ["TASK-038"]
assignee: Jules
---

### Descrição

Formulário de upload chamando `/api/documents/upload`. (Original TASK-013 do backlog)

### Critérios de Aceitação

- [ ] Componente de upload de arquivo PDF adicionado à `AnalisadorDocumentosPage.tsx`.
- [ ] Lógica para chamar o serviço `api.ts` para o endpoint `/api/documents/upload` implementada.

### Arquivos Relevantes

* `frontend/src/pages/AnalisadorDocumentosPage.tsx`
* `frontend/src/services/api.ts`

### Relatório de Execução

A interface de upload de documentos foi desenvolvida para a página 'Analisador de Documentos'.
    - **Serviço API (`frontend/src/services/api.ts`)**:
        - Adicionada a interface `DocumentUploadResponse` para a resposta do upload.
        - Criada a função `uploadDocumentForAnalysis(file: File)` que envia o arquivo para o endpoint `POST /api/documents/upload` usando `FormData` e lida com a resposta, incluindo o `task_id`.
    - **Componente de Formulário (`frontend/src/modules/analisador_documentos/components/DocumentUploadForm.tsx`)**:
        - Criado um novo componente React com MUI para o formulário de upload.
        - Inclui um input de arquivo PDF, botão de upload, e exibe o nome do arquivo selecionado.
        - Gerencia o estado local para o arquivo, status de carregamento e mensagens de feedback (sucesso/erro/task_id) usando `useState`.
        - Chama `uploadDocumentForAnalysis` ao submeter.
    - **Página Principal (`frontend/src/pages/AnalisadorDocumentosPage.tsx`)**:
        - O componente `DocumentUploadForm` foi importado e integrado na seção de upload da página.
    Os critérios de aceitação foram atendidos.
