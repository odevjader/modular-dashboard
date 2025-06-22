---
id: TASK-057
title: "DEV (Fase 4 Piloto): Refatorar Frontend do `gerador_quesitos` para Upload via Gateway"
epic: "Fase 4: Módulo Piloto e Integração"
status: done
priority: medium
dependencies: ["TASK-013"]
assignee: Jules
---

### Descrição

Modificar a interface do usuário do módulo `gerador_quesitos` para utilizar o novo fluxo de upload de documentos através do endpoint gateway da API Principal (presumivelmente `/api/documents/upload` ou o novo `/api/v1/documents/upload-and-process` se este for o relevante para o `gerador_quesitos`). O objetivo é alinhar este módulo com a arquitetura de processamento de documentos centralizada.

### Critérios de Aceitação

- [x] Interface de upload de arquivo no `gerador_quesitos` (e.g., `frontend/src/modules/gerador_quesitos/`) modificada/implementada.
- [x] Frontend chama o endpoint gateway apropriado para upload de documentos. (Now calls `/api/v1/documents/upload-and-process`)
- [x] Frontend lida com o `task_id` (ou `document_id`) retornado pelo gateway. (Stores `ProcessedDocumentInfo` containing the ID)
- [x] A lógica subsequente no frontend do `gerador_quesitos` utiliza o `task_id`/`document_id` para interagir com o backend do módulo (que será refatorado na TASK-058). (Store now calls a new service function with the document ID)

### Arquivos Relevantes

* `frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx`
* `frontend/src/stores/geradorQuesitosStore.ts`
* `frontend/src/services/api.ts`

### Relatório de Execução
### Relatório de Execução

O frontend do módulo `gerador_quesitos` foi refatorado para utilizar o novo gateway de processamento de documentos (`/api/v1/documents/upload-and-process`).

1.  **`frontend/src/services/api.ts` Modificado**:
    *   Adicionada a interface `ProcessedDocumentInfo` para tipar a resposta do gateway.
    *   Implementada a função `uploadAndProcessPdf(file: File): Promise<ProcessedDocumentInfo>` que envia um arquivo para o endpoint `/api/v1/documents/upload-and-process` e retorna os dados do documento processado.
    *   Adicionada a interface `GerarQuesitosPayload` e uma função placeholder `postGerarQuesitosComReferenciaDeDocumento` para a futura chamada ao backend refatorado do `gerador_quesitos`. O endpoint antigo `postGerarQuesitos` foi comentado.

2.  **`frontend/src/stores/geradorQuesitosStore.ts` Refatorado**:
    *   O estado da store foi atualizado para incluir `processedDocumentInfo: ProcessedDocumentInfo | null` e `currentFileBeingProcessed: File | null`.
    *   A ação `generateQuesitos` foi renomeada para `fetchQuesitosFromServer`. Esta nova ação agora espera um `documentId` (e outros dados do formulário) e chama `postGerarQuesitosComReferenciaDeDocumento`.
    *   Uma nova ação `uploadAndProcessSinglePdfForQuesitos(file: File, ...)` foi criada. Ela primeiro chama `uploadAndProcessPdf` e, em caso de sucesso, usa o `id` do documento retornado para chamar `fetchQuesitosFromServer`.
    *   A lógica de `isLoading`, `error`, e outros estados foi ajustada para o novo fluxo de duas etapas (upload/processamento do PDF, depois geração de quesitos).

3.  **`frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx` Modificado**:
    *   O componente agora utiliza a nova ação `uploadAndProcessSinglePdfForQuesitos`.
    *   Na função `handleGerarQuesitos`, o componente agora processa apenas o primeiro arquivo da lista `selectedFiles` se múltiplos arquivos forem selecionados, informando o usuário sobre esta limitação (devido ao gateway atual aceitar um único arquivo por vez).
    *   A UI foi ligeiramente ajustada para exibir o nome do arquivo sendo processado e informações do documento processado durante o estado de carregamento.

Com estas alterações, o frontend do `gerador_quesitos` está preparado para o novo fluxo onde o processamento do PDF é delegado ao `pdf_processor_service` através do gateway. A interação final com o backend do `gerador_quesitos` (TASK-058) usará o ID do documento processado.
