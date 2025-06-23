---
id: TASK-009
title: "Fix Backend Gateway Handling of Transcriber Service Redirect"
epic: "Bugfix - Backend Gateway"
type: "bug"
status: done # Updated status
priority: high
dependencies: ["TASK-008"]
assignee: Jules
---

### Descrição

The backend API gateway mishandled HTTP 307 redirects from the internal `transcritor_pdf_service`. The gateway called the transcriber's `/process-pdf` endpoint without a trailing slash. The transcriber service, expecting a trailing slash (`.../process-pdf/`), issued a 307 redirect. The gateway then incorrectly propagated this 307 to the frontend without a `Location` header, causing the frontend request to fail.

The hostname for the transcriber service (`transcritor_pdf_service`) was confirmed to be the correct one for Docker inter-service communication, after initial discussion about using `localhost`.

The fix involved ensuring the gateway calls the `transcritor_pdf_service` with the correct URL, including the trailing slash on the path.

### Critérios de Aceitação

- [x] The gateway service code (`backend/app/modules/documents/services.py`) was located and analyzed.
- [x] The URL used by the gateway to call the `transcritor_pdf_service`'s `/process-pdf` endpoint was corrected to use a trailing slash (`/process-pdf/`).
- [x] The hostname/port used by the gateway (`transcritor_pdf_service:8002`) was confirmed as correct for the Docker environment.
- [x] After the fix, PDF uploads from the frontend (via `TASK-007`'s module) complete successfully without 307 or related errors (as confirmed by user testing).
- [x] `TASK-008` (tracking the frontend symptom of this bug) can be closed/resolved.

### Arquivos Relevantes

* `backend/app/modules/documents/services.py` (modified)

### Relatório de Execução

1.  **Located Service File:** Identified `backend/app/modules/documents/services.py` as the location of the `httpx` call to the transcriber service.
2.  **Analyzed Issue:** Confirmed through logs and discussion that the `transcritor_pdf_service` expects its `/process-pdf` endpoint to be called with a trailing slash (`.../process-pdf/`) and issues a 307 redirect if called without it. The gateway was not appending this slash and was then mishandling the redirect it received.
3.  **Hostname Clarification:** Initially considered changing hostname to `localhost` based on user input, but then reverted to `transcritor_pdf_service` after user confirmed Docker service name resolution conventions.
4.  **Applied Fix:** Modified the `TRANSCRIBER_SERVICE_URL` constant in `backend/app/modules/documents/services.py` from `http://transcritor_pdf_service:8002/process-pdf` to `http://transcritor_pdf_service:8002/process-pdf/`.
5.  **User Confirmation:** The user tested the change after rebuilding/restarting the backend and confirmed that the PDF upload from the frontend now works correctly. This resolves the issue described in this task and unblocks TASK-008.
