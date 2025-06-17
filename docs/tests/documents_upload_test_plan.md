# Test Plan: Document Upload Endpoint (`/api/documents/upload`)

## 1. Introduction

This document outlines the test plan for the `/api/documents/upload` endpoint in the 'documents' module. This endpoint allows authenticated users to upload files, which are then forwarded to the `transcritor-pdf` service for processing. This plan focuses on integration scenarios and complements the existing unit tests.

## 2. Scope

### In Scope:
*   Verification of successful file upload and forwarding to a mocked transcriber service.
*   Handling of authentication (valid and missing/invalid tokens).
*   Error handling for responses from the (mocked) `transcritor-pdf` service.
*   Basic input validation (e.g., presence of a file).

### Out of Scope:
*   Testing the `transcritor-pdf` service itself (it will be mocked).
*   Specific performance or load testing of the upload endpoint.
*   User interface testing for file uploads.
*   Detailed binary-level validation of PDF content integrity (unless basic FastAPI/Starlette validation catches it).

## 3. Test Objectives

*   Ensure authenticated users can successfully upload files.
*   Verify that unauthenticated or improperly authenticated requests are rejected.
*   Confirm that errors from the downstream `transcritor-pdf` service are handled gracefully and reported appropriately.
*   Document current behavior regarding different file types if no explicit server-side validation is implemented.

## 4. Test Scenarios

The following scenarios will be tested. Many of these are already covered by unit tests (`backend/tests/test_documents_module.py`), and this plan serves to formalize them from an integration perspective.

### Scenario 4.1: Successful File Upload

*   **Description**: An authenticated user uploads a valid file (e.g., PDF). The system successfully forwards it to the (mocked) `transcritor-pdf` service, which returns a success response.
*   **Preconditions**:
    *   User is authenticated with a valid JWT token.
    *   The `transcritor-pdf` service (mocked at the HTTP client level) is configured to return a 200 OK response with expected JSON payload.
*   **Test Steps**:
    1.  Obtain a valid authentication token.
    2.  Send a `POST` request to `/api/documents/upload` with:
        *   `Authorization: Bearer <token>` header.
        *   Multipart form data including a file (e.g., `test.pdf` with `content_type: application/pdf`).
*   **Expected Result**:
    *   HTTP Status Code: 200 OK.
    *   Response body: JSON indicating success, including original filename, a message, and data from the mocked transcriber service (as per current implementation: `{"filename": "test.pdf", "message": "File successfully processed by transcriber.", "transcriber_data": {...}, "uploader_user_id": X}`).
*   **Unit Test Coverage**: Covered by `test_upload_document_success`.

### Scenario 4.2: Authentication Failure - Missing Token

*   **Description**: An attempt is made to upload a file without an authentication token.
*   **Preconditions**: None.
*   **Test Steps**:
    1.  Send a `POST` request to `/api/documents/upload` with multipart form data (a file) but **without** an `Authorization` header.
*   **Expected Result**:
    *   HTTP Status Code: 401 Unauthorized.
    *   Response body: JSON detailing the authentication error (e.g., `{"detail":"Not authenticated"}`).
*   **Unit Test Coverage**: Implicitly covered by FastAPI's `Depends(get_current_active_user)`. Can be explicitly tested with `TestClient` by not setting auth.

### Scenario 4.3: Authentication Failure - Invalid Token

*   **Description**: An attempt is made to upload a file with an invalid or expired authentication token.
*   **Preconditions**: None.
*   **Test Steps**:
    1.  Send a `POST` request to `/api/documents/upload` with:
        *   `Authorization: Bearer <invalid_token>` header.
        *   Multipart form data including a file.
*   **Expected Result**:
    *   HTTP Status Code: 401 Unauthorized.
    *   Response body: JSON detailing the authentication error (e.g., `{"detail":"Could not validate credentials"}`).
*   **Unit Test Coverage**: Implicitly covered by FastAPI's `Depends(get_current_active_user)`. Can be explicitly tested.

### Scenario 4.4: Transcriber Service Error - HTTPStatusError (e.g., 4xx/5xx)

*   **Description**: The `transcritor-pdf` service (mocked) returns an HTTP error (e.g., 422 Unprocessable Entity, 500 Internal Server Error).
*   **Preconditions**:
    *   User is authenticated.
    *   The mocked `transcritor-pdf` service is configured to return an error status code (e.g., 422).
*   **Test Steps**:
    1.  Obtain a valid authentication token.
    2.  Send a `POST` request to `/api/documents/upload` with a file and valid auth.
*   **Expected Result**:
    *   HTTP Status Code: Matches the error code returned by the mocked service (e.g., 422).
    *   Response body: JSON detailing the error, likely propagated from the transcriber service. (e.g., `{"detail":"Error from transcriber service: Status 422 - {"detail":"Invalid PDF content"}"}`).
*   **Unit Test Coverage**: Covered by `test_upload_document_transcriber_error`.

### Scenario 4.5: Transcriber Service Error - Connection Error

*   **Description**: The API gateway is unable to connect to the `transcritor-pdf` service (e.g., network issue, service down).
*   **Preconditions**:
    *   User is authenticated.
    *   The mocked `httpx.AsyncClient.post` is configured to raise an `httpx.RequestError`.
*   **Test Steps**:
    1.  Obtain a valid authentication token.
    2.  Send a `POST` request to `/api/documents/upload` with a file and valid auth.
*   **Expected Result**:
    *   HTTP Status Code: 503 Service Unavailable.
    *   Response body: JSON detailing the connection error (e.g., `{"detail":"Service unavailable: Could not connect to transcriber service: Connection failed"}`).
*   **Unit Test Coverage**: Covered by `test_upload_document_transcriber_connection_error`.

### Scenario 4.6: Invalid File Type / Content (Current Behavior)

*   **Description**: An authenticated user uploads a file that is not a PDF, or a file that is not expected by the `transcritor-pdf` service.
*   **Note**: The `/api/documents/upload` endpoint, as implemented in TASK-013, does not perform explicit server-side validation of the `UploadFile.content_type` or file magic numbers beyond what FastAPI/Starlette provide by default for `UploadFile`. The `transcritor-pdf` service is assumed to handle validation of the content it receives.
*   **Preconditions**:
    *   User is authenticated.
*   **Test Steps**:
    1.  Obtain a valid authentication token.
    2.  Send a `POST` request to `/api/documents/upload` with:
        *   A file that is not a PDF (e.g., `test.txt` with `content_type: text/plain` or `test.jpg` with `content_type: image/jpeg`).
*   **Expected Result (Current Behavior)**:
    *   The file will likely be forwarded to the `transcritor-pdf` service.
    *   The response will depend on how the (mocked or real) `transcritor-pdf` service handles unexpected file types.
        *   If the mocked transcriber is benign: HTTP 200 OK from `/api/documents/upload`, with the transcriber's (mocked) response.
        *   If the (mocked) transcriber returns an error (e.g., 400 or 422): The `/api/documents/upload` endpoint will return that error, as per Scenario 4.4.
    *   **Conclusion**: No specific validation for file type is implemented at the gateway level in TASK-013. This scenario documents current behavior. Future enhancements could add such validation.
*   **Unit Test Coverage**: Not explicitly tested for various file types, as the focus was on forwarding. Unit tests use `application/pdf`.

### Scenario 4.7: Missing File in Upload

*   **Description**: An authenticated user attempts to call the endpoint without providing a file.
*   **Preconditions**: User is authenticated.
*   **Test Steps**:
    1.  Obtain a valid authentication token.
    2.  Send a `POST` request to `/api/documents/upload` with `Authorization` header but **no file** in the multipart form data.
*   **Expected Result**:
    *   HTTP Status Code: 422 Unprocessable Entity (FastAPI's default for missing required `File` parameter).
    *   Response body: JSON detailing the validation error (e.g., field required).
*   **Unit Test Coverage**: Can be added; standard FastAPI validation behavior.

## 5. Test Environment and Tools

*   **Unit/Integration Tests**: `pytest` with `TestClient` from FastAPI. Mocking via `unittest.mock`.
*   **Manual API Testing (Optional)**: Tools like Postman or `curl` against a running instance with a mocked `transcritor-pdf` service if deeper, non-unit integration is needed.
*   **Dependencies**: Python, FastAPI, httpx, etc., as per `requirements.txt`.

## 6. Responsibilities

*   **Test Plan Creation**: Jules (AI Agent)
*   **Test Execution (Unit/Integration)**: Automated via CI/CD pipeline or manually by developers running `pytest`.
*   **Test Execution (Manual, if applicable)**: Developer/QA.

## 7. Success Criteria for this Test Plan

*   All documented test scenarios are executed.
*   Actual results match expected results for critical paths (successful upload, auth failure).
*   Deviations or failures are documented and reported for remediation.
