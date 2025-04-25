#docs/plan/issue_17_refactor_health_plan.md
# Plan: Refactor Health Module (Issue #17)

This document outlines the plan to refactor the `health` module from `backend/app/modules/` to `backend/app/core_modules/` as part of Issue #17.

**Approved Plan Steps:**

1.  **Create New Directory Structure:**
    *   Create the directory `backend/app/core_modules/health/`.
    *   Create the subdirectory `backend/app/core_modules/health/v1/`.

2.  **Move Endpoint File:**
    *   Move the file `backend/app/modules/health/v1/endpoints.py` to the new location: `backend/app/core_modules/health/v1/endpoints.py`.

3.  **Update Import in API Router:**
    *   Modify the file `backend/app/api_router.py`.
    *   Change line 5 from:
        ```python
        from app.modules.health.v1 import endpoints as health_v1_endpoints
        ```
        to:
        ```python
        from app.core_modules.health.v1 import endpoints as health_v1_endpoints
        ```

4.  **Add Header Comments (Standardization):**
    *   Ensure the moved file `backend/app/core_modules/health/v1/endpoints.py` has the comment `#backend/app/core_modules/health/v1/endpoints.py` as its first line.
    *   Ensure the modified file `backend/app/api_router.py` retains its header comment `#backend/app/api_router.py` on the first line.

5.  **Remove Old Directory:**
    *   Delete the original directory `backend/app/modules/health/` (including its `v1` subdirectory).

6.  **Verification (To be performed by Dev):**
    *   After the changes are applied, the Dev needs to verify:
        *   The FastAPI application starts without errors.
        *   The health check endpoint (`/api/health/v1`) is accessible and returns a successful response.

**Visualization (Mermaid Sequence Diagram):**

```mermaid
sequenceDiagram
    participant Coder as AI Coder (Architect Mode)
    participant Dev as Developer (Human)
    participant FS as Filesystem
    participant API as FastAPI App

    Coder->>FS: 1. Create dir `backend/app/core_modules/health/v1/`
    Coder->>FS: 2. Move `backend/app/modules/health/v1/endpoints.py` to `backend/app/core_modules/health/v1/`
    Coder->>FS: 3. Modify `backend/app/api_router.py` (update import line 5)
    Coder->>FS: 4. Add/Verify header comments in moved/modified files
    Coder->>FS: 5. Delete dir `backend/app/modules/health/`
    Coder->>Dev: Request Verification
    Dev->>API: 6. Start FastAPI App
    API-->>Dev: Report Status (Success/Error)
    Dev->>API: 6. Access /api/health/v1 endpoint
    API-->>Dev: Return Health Status
    Dev->>Coder: Confirm Verification Result