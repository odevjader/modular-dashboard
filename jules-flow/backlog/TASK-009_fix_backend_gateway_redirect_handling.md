---
id: TASK-009
title: "Fix Backend Gateway Handling of Transcriber Service Redirect"
epic: "Bugfix - Backend Gateway"
type: "bug"
status: backlog
priority: high
dependencies: ["TASK-008"]
assignee: Jules
---

### Descrição

The backend API gateway currently mishandles HTTP 307 redirects received from the internal `transcritor_pdf_service`.
The sequence of events is:
1.  Gateway calls `transcritor_pdf_service` at an endpoint like `http://<transcriber_host>:<port>/process-pdf` (without a trailing slash).
2.  The `transcritor_pdf_service` expects this endpoint with a trailing slash (`.../process-pdf/`) and issues a 307 redirect to the slashed version, correctly including a `Location` header.
3.  The gateway's `httpx` client receives this 307. Instead of following the redirect or proxying it correctly, its error handling logic creates a *new* FastAPI `HTTPException` with status 307 but **omits the `Location` header**, sending only a JSON body (`{"detail":"Error from transcriber service: Status 307."}`) back to the frontend.
4.  This causes the frontend `fetch` to fail as it receives a 307 without a `Location`.

Additionally, the user has indicated that the hostname `transcritor_pdf_service` used by the gateway might be incorrect in the Docker environment, and `http://localhost:8002/` might be the intended target for the transcriber service from the gateway's perspective. This also needs to be verified and corrected in the gateway's service call.

The primary fix is to ensure the gateway calls the `transcritor_pdf_service` with the correct URL, including the correct hostname/port and the trailing slash on the path.

### Critérios de Aceitação

- [ ] The gateway service code (`backend/app/modules/documents/services.py` or similar) is located and analyzed.
- [ ] The URL used by the gateway to call the `transcritor_pdf_service`'s `/process-pdf` endpoint is corrected to use a trailing slash (`/process-pdf/`).
- [ ] The hostname/port used by the gateway to call the `transcritor_pdf_service` is verified and corrected if necessary (e.g., if `transcritor_pdf_service` should indeed be `localhost` from the gateway's container perspective, or if it should be configured via environment variables).
- [ ] After the fix, PDF uploads from the frontend (via `TASK-007`'s module) complete successfully without 307 or related errors.
- [ ] `TASK-008` (tracking the frontend symptom of this bug) can be closed/resolved.

### Arquivos Relevantes

* `backend/app/modules/documents/services.py` (or the actual file in the `backend/` folder that makes the call to the transcriber service)
* Backend logs previously provided by the user.

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
