# Test Plan: `POST /process-pdf` Endpoint (Transcritor Service)

## 1. Introduction

*   **1.1. Purpose**: To define the test strategy and scope for verifying the functionality of the `POST /process-pdf` endpoint in the `transcritor-pdf` service.
*   **1.2. Scope**:
    *   Testing focuses on the API endpoint itself: its ability to accept valid PDF file uploads, validate inputs, queue a Celery task for processing, and return appropriate HTTP responses.
    *   Verification of the successful *execution* of the Celery task and the correctness of the downstream PDF processing pipeline (text extraction, embedding, storage) is out of scope for *this specific test plan*.
*   **1.3. Document Version**: 1.0
*   **1.4. References**:
    *   TASK-020: DEV: Implementar Endpoint de Processamento de PDF no Transcritor-PDF
    *   TASK-021: TEST-PLAN: Planejar Testes para Endpoint `process-pdf` (Transcritor)
    *   `transcritor-pdf/src/main.py` (source code for the endpoint)

## 2. Test Environment and Setup

*   **2.1. Service Endpoint**: `http://<host_transcritor_pdf>:<port_transcritor_pdf>/process-pdf/` (Replace placeholders with actual values during testing, e.g., `http://localhost:8000/process-pdf/` if running locally via default uvicorn command in `main.py`)
*   **2.2. Prerequisites**:
    *   The `transcritor-pdf` FastAPI application must be running.
    *   A Celery worker configured to listen to the queue used by `transcritor-pdf` must be running.
    *   A Redis instance (or other configured Celery broker) must be running and accessible.
    *   Environment variables for the `transcritor-pdf` service must be correctly set (e.g., `OPENAI_API_KEY` for downstream processing, Celery broker URL, database connection details for `main.py` startup).
*   **2.3. Tools**:
    *   API client tool (e.g., `curl`, Postman, Insomnia).
    *   (Optional) Python testing script with `httpx` or `requests`.
    *   (Optional) Celery monitoring tool (e.g., Flower) or direct log inspection to observe task queuing.
*   **2.4. Test Data (Assumed to be available in a `test_files/` directory or similar)**:
    *   `sample.pdf`: A small, valid, single-page or multi-page PDF document.
    *   `empty.pdf`: A 0-byte PDF file.
    *   `textfile.txt`: A plain text file.
    *   `image.jpg`: An image file (e.g., JPEG).
    *   `corrupted.pdf` (Optional): A PDF file known to be corrupted in a way that might cause issues during `file.read()`.
    *   `large.pdf` (Optional): A valid PDF file of significant size (e.g., 50MB+) to observe handling of larger uploads.

## 3. Test Strategy

*   **3.1. Testing Levels**: API / Integration Testing (focusing on the endpoint's interaction with request data and Celery).
*   **3.2. Testing Types**:
    *   Functional Testing (Happy Path, Error Handling).
    *   Negative Testing (Invalid Inputs).
*   **3.3. Mocking / Verification of Task Queuing**:
    *   **Direct Observation**: Check Celery worker logs or use a tool like Flower to confirm that a task with the expected arguments is received after a successful API call.
    *   **Mocking (for automated tests)**: If writing automated Python tests, `process_pdf_task.delay` could be mocked using `unittest.mock.patch` to assert it's called with the correct `file_content_bytes` and `filename` without actually queuing the task.

## 4. Test Cases

### 4.1. Scenario: Successful PDF Upload and Task Queuing

*   **TC_PDF_001: Valid PDF Upload**
    *   **Description**: Verify that a valid PDF file is accepted and a Celery task is successfully queued.
    *   **Preconditions**: `transcritor-pdf` service and Celery worker are running. `sample.pdf` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `sample.pdf` in the `file` field.
    *   **Test Data**: `sample.pdf`
    *   **Expected Result**:
        *   HTTP Status Code: 200 OK.
        *   Response Body (JSON): `{"task_id": "<some_celery_task_id>", "message": "PDF processing has been queued. You can check the status using the /process-pdf/status/{task_id} endpoint (not yet implemented)."}`
        *   Celery Task: `process_pdf_task` is queued with the content of `sample.pdf` and its filename.

### 4.2. Scenario: Invalid File Type (Non-PDF)

*   **TC_PDF_002: Upload Text File**
    *   **Description**: Verify that uploading a `.txt` file results in a 415 error.
    *   **Preconditions**: `transcritor-pdf` service is running. `textfile.txt` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `textfile.txt` in the `file` field.
    *   **Test Data**: `textfile.txt`
    *   **Expected Result**:
        *   HTTP Status Code: 415 Unsupported Media Type.
        *   Response Body (JSON): `{"detail": "Invalid file type. Only PDF files are allowed."}`

*   **TC_PDF_003: Upload Image File**
    *   **Description**: Verify that uploading a `.jpg` file results in a 415 error.
    *   **Preconditions**: `transcritor-pdf` service is running. `image.jpg` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `image.jpg` in the `file` field.
    *   **Test Data**: `image.jpg`
    *   **Expected Result**:
        *   HTTP Status Code: 415 Unsupported Media Type.
        *   Response Body (JSON): `{"detail": "Invalid file type. Only PDF files are allowed."}`

### 4.3. Scenario: Empty File Upload (0 Bytes PDF)

*   **TC_PDF_004: Upload Empty PDF**
    *   **Description**: Verify that uploading an empty (0 bytes) PDF file results in a 400 error.
    *   **Preconditions**: `transcritor-pdf` service is running. `empty.pdf` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `empty.pdf` in the `file` field.
    *   **Test Data**: `empty.pdf`
    *   **Expected Result**:
        *   HTTP Status Code: 400 Bad Request.
        *   Response Body (JSON): `{"detail": "Uploaded file is empty."}`

### 4.4. Scenario: No Filename Provided (Simulated)

*   **TC_PDF_005: Upload File with No Filename**
    *   **Description**: Verify that if an `UploadFile` object has no filename, a 400 error is returned. (This might require specific client behavior or mocking to simulate if standard clients always send a name).
    *   **Preconditions**: `transcritor-pdf` service is running.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data` where the `file` part's filename is empty or not set.
    *   **Test Data**: File content with no associated filename in the request part header.
    *   **Expected Result**:
        *   HTTP Status Code: 400 Bad Request.
        *   Response Body (JSON): `{"detail": "No filename provided."}`

### 4.5. Scenario: Request Without a File

*   **TC_PDF_006: Missing File in Request**
    *   **Description**: Verify that sending a request without a file in the `file` field results in a 422 error.
    *   **Preconditions**: `transcritor-pdf` service is running.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data` but without including a `file` part.
    *   **Test Data**: N/A (form data is missing the 'file' field).
    *   **Expected Result**:
        *   HTTP Status Code: 422 Unprocessable Entity.
        *   Response Body (JSON): FastAPI's standard validation error response for a missing required form field (e.g., `{"detail":[{"loc":["body","file"],"msg":"field required","type":"value_error.missing"}]}`).

### 4.6. Scenario: Corrupted PDF (Endpoint Behavior Only)

*   **TC_PDF_007 (Optional): Upload Corrupted PDF Causing Read Error**
    *   **Description**: Verify the endpoint's behavior if reading the file bytes causes an immediate error before task queuing.
    *   **Preconditions**: `transcritor-pdf` service is running. `corrupted.pdf` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `corrupted.pdf` (designed to fail on `file.read()`) in the `file` field.
    *   **Test Data**: `corrupted.pdf`
    *   **Expected Result**:
        *   HTTP Status Code: 500 Internal Server Error.
        *   Response Body (JSON): `{"detail": "An internal server error occurred while processing the PDF: corrupted.pdf."}` (or similar, depending on the exact error and how it's caught by the endpoint's generic exception handler).

### 4.7. Scenario: Large PDF File (Conceptual - Endpoint Queuing)

*   **TC_PDF_008 (Conceptual/Non-Functional): Upload Large PDF**
    *   **Description**: Observe the endpoint's ability to handle a large PDF upload and queue the task.
    *   **Preconditions**: `transcritor-pdf` service and Celery worker are running. `large.pdf` is available.
    *   **Test Steps**:
        1.  Send a `POST` request to `/process-pdf/` with `multipart/form-data`.
        2.  Include `large.pdf` in the `file` field.
    *   **Test Data**: `large.pdf`
    *   **Expected Result**:
        *   HTTP Status Code: 200 OK.
        *   Response Body (JSON): Contains `task_id`.
        *   Celery Task: `process_pdf_task` is queued.
        *   **Observations**: Note time taken for the request, memory usage of the service during upload (if possible). This is more of an observation for potential performance issues than a strict pass/fail on functionality beyond queuing.

## 5. Success Criteria

*   All defined mandatory test cases (TC_PDF_001 to TC_PDF_006) pass as per their expected results.
*   The endpoint remains stable and responsive throughout testing.
*   Celery task queuing is successfully verified for valid inputs.

## 6. Out of Scope

*   Detailed verification of the PDF content processing by the Celery task (e.g., accuracy of text extraction, correctness of embeddings, database integrity after storage). This should be covered by tests for the `process_pdf_pipeline` and downstream components.
*   Load or stress testing beyond the conceptual large file upload.
*   Security vulnerability testing.
*   User interface testing (this is an API test plan).

## 7. Test Reporting (Placeholder)

*   *(This section will be filled in upon actual test execution.)*
    *   **Test Execution Summary**: Date, Tester, Environment, etc.
    *   **Results per Test Case**: (e.g., TC_PDF_001: Passed, TC_PDF_002: Passed, etc.)
    *   **Defects Found**: List any defects encountered, with IDs if applicable.
    *   **Overall Assessment**: Pass/Fail based on success criteria.
