---
id: TASK-008
title: "Fix 307 Temporary Redirect Error on PDF Upload"
epic: "Bugfix - Frontend/Gateway Integration"
type: "bug" # Assuming 'bug' is a valid type, else 'development'
status: backlog
priority: high
dependencies: ["TASK-007"] # Depends on the frontend tester module being in place
assignee: Jules
---

### Descrição

When uploading a PDF using the "Transcritor PDF - Tester" frontend module, the API request to `/api/documents/upload` fails with a `307 Temporary Redirect` error. The full error message observed was: `API request failed: 307 Temporary Redirect - {"detail":"Error from transcriber service: Status 307."}`.

This task is to investigate the cause of this redirect and implement a fix, likely in the frontend's API call, or to identify necessary backend changes. A common cause for 307 on POST requests is a mismatch in trailing slashes between the client request and the server's expectation.

### Critérios de Aceitação

- [ ] The root cause of the 307 redirect is identified.
- [ ] PDF upload via the "Transcritor PDF - Tester" module no longer results in a 307 error.
- [ ] The transcription process is successfully initiated after a PDF upload.
- [ ] If the fix is frontend-only, it is implemented and tested.
- [ ] If the fix requires backend changes, these changes are clearly documented and communicated.

### Arquivos Relevantes

* `frontend/src/services/api.ts` (specifically `uploadDocumentForAnalysis` function)
* `frontend/vite.config.ts` (for proxy configuration review)
* Potentially backend API documentation or gateway configuration (for user to check)

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
