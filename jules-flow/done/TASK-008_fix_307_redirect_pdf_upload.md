---
id: TASK-008
title: "Fix 307 Temporary Redirect Error on PDF Upload"
epic: "Bugfix - Frontend/Gateway Integration"
type: "bug"
status: done # Updated status
priority: high
dependencies: ["TASK-007"]
assignee: Jules
---

### Descrição

When uploading a PDF using the "Transcritor PDF - Tester" frontend module, the API request to `/api/documents/upload` (made by the frontend to the gateway) failed with a `307 Temporary Redirect` error. The response body from the gateway was `{"detail":"Error from transcriber service: Status 307."}`, but this 307 response from the gateway critically lacked a `Location` header.

### Investigation Findings & Root Cause

The issue stemmed from the backend API gateway's handling of an internal redirect from the `transcritor_pdf_service`.
1.  The frontend correctly calls the gateway at `/api/documents/upload` (no trailing slash).
2.  The gateway then makes an internal HTTP POST request (using `httpx`) to the `transcritor_pdf_service` at `http://transcritor_pdf_service:8002/process-pdf` (also no trailing slash).
3.  The `transcritor_pdf_service` expects its `/process-pdf` endpoint to be called with a trailing slash (`.../process-pdf/`). It therefore responds to the gateway's internal request with a standard HTTP 307 redirect, including a `Location: http://transcritor_pdf_service:8002/process-pdf/` header.
4.  The gateway's `httpx` client receives this 307. Its error handling (in `/app/app/modules/documents/services.py`, corresponding to `backend/app/modules/documents/services.py` in the repo) caught the `httpx.HTTPStatusError`.
5.  Instead of following this internal redirect or correctly proxying the redirect, the gateway constructed a *new* `fastapi.exceptions.HTTPException` with status 307 but **omitted the `Location` header**.
6.  The frontend received this malformed 307 response and could not process it.

This was identified as a backend issue within the API gateway service.

### Critérios de Aceitação

- [x] The root cause of the 307 redirect is identified.
- [x] PDF upload via the "Transcritor PDF - Tester" module no longer results in a 307 error (Resolved by backend fix in TASK-009).
- [x] The transcription process is successfully initiated after a PDF upload (Resolved by backend fix in TASK-009).
- [x] If the fix is frontend-only, it is implemented and tested. (No frontend fix was applicable).
- [x] If the fix requires backend changes, these changes are clearly documented and communicated (Documented and fixed in TASK-009).

### Arquivos Relevantes (Frontend Investigation)

* `frontend/src/services/api.ts` (investigated, no changes needed from its original state for this bug)
* `frontend/vite.config.ts` (reviewed)

### Relatório de Execução (Frontend Investigation & Resolution)

1.  **Initial Error:** Frontend received a 307 from `/api/documents/upload` with a JSON body and no `Location` header.
2.  **Diagnostic Steps:**
    *   Tested calling gateway with/without trailing slash from frontend.
    *   Used `redirect: 'manual'` in frontend `fetch` to inspect redirect behavior.
    *   Analyzed backend logs provided by the user.
3.  **Root Cause Identified:** The backend gateway was calling the `transcritor_pdf_service` at `.../process-pdf` (no slash). The transcriber service responded with a 307 to `.../process-pdf/` (with slash) including a `Location` header. The gateway then created a new 307 response for the frontend but omitted this `Location` header.
4.  **Resolution:** The issue was resolved by `TASK-009`, which involved correcting the call in the backend gateway (`backend/app/modules/documents/services.py`) to use the trailing slash when calling the `transcritor_pdf_service`. Specifically, `TRANSCRIBER_SERVICE_URL` was changed to `http://transcritor_pdf_service:8002/process-pdf/`.
5.  **User Confirmation:** User tested after the backend fix (TASK-009) and confirmed the PDF upload now works correctly.

This task is now considered done as the underlying issue has been fixed in the backend as part of TASK-009.
