---
id: TASK-008
title: "Fix 307 Temporary Redirect Error on PDF Upload"
epic: "Bugfix - Frontend/Gateway Integration"
type: "bug"
status: blocked # Changed status to blocked, pending backend changes
priority: high
dependencies: ["TASK-007"]
assignee: Jules
---

### Descrição

When uploading a PDF using the "Transcritor PDF - Tester" frontend module, the API request to `/api/documents/upload` (made by the frontend to the gateway) fails with a `307 Temporary Redirect` error. The response body from the gateway is `{"detail":"Error from transcriber service: Status 307."}`, but this 307 response from the gateway critically lacks a `Location` header.

### Investigation Findings & Root Cause

The issue stems from the backend API gateway's handling of an internal redirect from the `transcritor_pdf_service`.
1.  The frontend correctly calls the gateway at `/api/documents/upload` (no trailing slash).
2.  The gateway then makes an internal HTTP POST request (using `httpx`) to the `transcritor_pdf_service` at `http://transcritor_pdf_service:8002/process-pdf` (also no trailing slash).
3.  The `transcritor_pdf_service` expects its `/process-pdf` endpoint to be called with a trailing slash (`.../process-pdf/`). It therefore responds to the gateway's internal request with a standard HTTP 307 redirect, including a `Location: http://transcritor_pdf_service:8002/process-pdf/` header.
4.  The gateway's `httpx` client receives this 307. Its error handling (in `/app/app/modules/documents/services.py`) catches the `httpx.HTTPStatusError` (as 307 is not a 2xx success code).
5.  Instead of following this internal redirect or correctly proxying the redirect (with its `Location` header) back to the frontend, the gateway constructs a *new* `fastapi.exceptions.HTTPException`. It sets the status code of this new exception to 307 but **fails to include the `Location` header**. It only includes the JSON body `{"detail":"Error from transcriber service: Status 307."}`.
6.  The frontend receives this malformed 307 response (no `Location` header) and cannot process it as a redirect, leading to the observed error.

**This is a backend issue within the API gateway service.**

### Critérios de Aceitação

- [x] The root cause of the 307 redirect is identified.
- [ ] PDF upload via the "Transcritor PDF - Tester" module no longer results in a 307 error (Pending backend fix).
- [ ] The transcription process is successfully initiated after a PDF upload (Pending backend fix).
- [ ] If the fix is frontend-only, it is implemented and tested. (No frontend fix applicable beyond diagnostics, which have been reverted).
- [x] If the fix requires backend changes, these changes are clearly documented and communicated (documented herein).

### Arquivos Relevantes (Frontend)

* `frontend/src/services/api.ts` (investigated, no changes needed from its original state for this bug)
* `frontend/vite.config.ts` (reviewed)

### Relatório de Execução (Frontend Investigation)

1.  **Initial Error:** Frontend received a 307 from `/api/documents/upload` with a JSON body and no `Location` header.
2.  **Trailing Slash Test:** Modified frontend to call `/api/documents/upload/`. This led to the gateway redirecting *back* to `/api/documents/upload` (no slash), and the browser stripping the `Authorization` header on this redirect, causing a 401. This indicated the gateway itself prefers no trailing slash for its exposed endpoint.
3.  **Manual Redirect Handling Test:** Modified frontend `fetch` with `redirect: 'manual'`. This confirmed the 307 from `/api/documents/upload` (Vite proxy) had no `Location` header in its response to the browser.
4.  **Backend Log Analysis:** User provided backend logs which showed:
    *   Gateway calls `transcritor_pdf_service` at `.../process-pdf` (no slash).
    *   `transcritor_pdf_service` responds with 307 and `Location: .../process-pdf/` (with slash).
    *   Gateway converts this into a new FastAPI HTTP 307 Exception but omits the `Location` header.
5.  **Conclusion:** The frontend is calling the gateway correctly. The gateway needs to be fixed.
    *   **Recommended Fix for Backend Gateway (`/app/app/modules/documents/services.py`):**
        1.  **Option A (Preferred):** Change the `httpx` call to the `transcritor_pdf_service` to use the URL with a trailing slash: `http://transcritor_pdf_service:8002/process-pdf/`.
        2.  **Option B:** Configure the `httpx` client in the gateway to automatically follow redirects from the `transcritor_pdf_service` (e.g., using `follow_redirects=True` for the client or request).
6.  **Frontend Reverted:** Diagnostic changes in `frontend/src/services/api.ts` (trailing slash, `redirect:'manual'`, extra logging) have been reverted. No frontend code changes are required to fix this bug.

The task status is now `blocked` pending the backend gateway fix.Tool output for `overwrite_file_with_block`:
