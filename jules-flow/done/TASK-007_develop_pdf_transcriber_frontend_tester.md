---
id: TASK-007
title: "Develop Frontend Module for PDF Transcriber Testing (Transcritor PDF - Tester)"
epic: "Frontend Development"
type: "development"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Develop a frontend interface to test the `transcritor-pdf` microservice. This module, named "Transcritor PDF - Tester", will allow users to upload a PDF file, monitor the transcription progress via its task ID, and view the final transcription result.

### Critérios de Aceitação

- [x] Existing frontend structure in the `frontend` folder is understood and documented.
- [x] A new module "Transcritor PDF - Tester" is created under `frontend/src/modules/pdf_transcriber_tester/`.
- [x] The new module is registered in `frontend/src/config/moduleRegistry.ts` with the name "Transcritor PDF - Tester", a base path of `/pdf-transcriber`, and is accessible via routing.
- [x] The module page (`PdfTranscriberTesterPage.tsx`) provides a UI for users to select a PDF file.
- [x] The module allows users to upload the selected PDF file to the backend service using `uploadDocumentForAnalysis` from `api.ts`.
- [x] After successful upload, the module displays the returned `task_id`.
- [x] The module polls the `/documents/upload/status/{task_id}` endpoint (via `getTaskStatus` from `api.ts`) to get the transcription status.
- [x] The module displays the current transcription status (e.g., PENDING, PROCESSING, SUCCESS, FAILURE).
- [x] If transcription is successful, the module displays the resulting transcription text.
- [x] Appropriate loading indicators (CircularProgress) and error/success messages (Snackbar notifications) are displayed to the user.

### Arquivos Relevantes

* `frontend/src/config/moduleRegistry.ts` (updated)
* `frontend/src/services/api.ts` (used)
* `frontend/src/modules/pdf_transcriber_tester/PdfTranscriberTesterPage.tsx` (created and implemented)

### Relatório de Execução

1.  **Module Creation & Registration:**
    *   Created the directory `frontend/src/modules/pdf_transcriber_tester/`.
    *   Created the main component `PdfTranscriberTesterPage.tsx` within this directory.
    *   Registered the module in `frontend/src/config/moduleRegistry.ts` with:
        *   `name: 'Transcritor PDF - Tester'`
        *   `basePath: '/pdf-transcriber'`
        *   `navIcon: DescriptionIcon`
        *   `navText: 'Transcritor PDF'`
        *   Route pointing to the lazy-loaded `PdfTranscriberTesterPage`.

2.  **UI Implementation (`PdfTranscriberTesterPage.tsx`):**
    *   Used Material-UI components (`Container`, `Paper`, `Typography`, `Button`, `TextField` for file input, `CircularProgress`, `Alert`) for the UI.
    *   The UI includes:
        *   A file input field for PDF selection.
        *   An "Upload & Transcribe" button.
        *   Display areas for the selected filename, upload status, Task ID, transcription status, and the final transcription result (in a read-only multiline TextField).

3.  **State Management & Logic:**
    *   Managed component state using `React.useState` for `selectedFile`, `uploadStatus`, `taskId`, `transcriptionStatus`, `transcriptionResult`, loading states (`isUploading`, `isPolling`), and error messages.
    *   Implemented `handleFileChange` to update the selected file and reset states.
    *   Implemented `handleUpload` to call the `uploadDocumentForAnalysis` API function, handle its response (extracting `task_id`), and manage upload states.
    *   Implemented a `useEffect` hook with a `useCallback` memoized polling function (`pollStatus`) to periodically call `getTaskStatus` API for the given `task_id`. Polling stops on "SUCCESS" or "FAILURE" status or if an error occurs during polling.
    *   Integrated `useSnackbar` from `notistack` for user notifications for events like file selection warnings, upload success/failure, transcription completion, and polling errors.

4.  **Styling & Responsiveness:**
    *   Leveraged MUI's built-in responsiveness and styling. `Grid` components were used for layout, ensuring elements adapt to different screen sizes.

The module should now be functional and allow users to test the PDF transcription service. Further testing in a running environment is recommended to confirm all interactions.
