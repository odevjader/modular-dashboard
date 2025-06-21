# Test Plan: PDF Processing Pipeline

**Document Version:** 1.0
**Date:** 2025-06-21

## 1. Overview

This document outlines the test plan for the PDF Processing Pipeline, which includes:
- The `pdf_processor_service` microservice.
- The API Gateway endpoint `/api/v1/documents/upload-and-process` in the main backend.

The goal is to ensure the reliability, correctness, and robustness of PDF uploading, text extraction, chunking, storage, and the interaction between the gateway and the microservice.

## 2. Scope of Testing

### 2.1. `pdf_processor_service`

#### 2.1.1. Unit Tests

-   **`extraction_service.py`**:
    -   `generate_file_hash()`:
        - Test with known byte content for consistent hash output.
        - Test with empty byte content.
    -   `extract_text_from_pdf()`:
        - Test with a simple, valid PDF (bytes): verify extracted text matches expected.
        - Test with a multi-page PDF: verify text from all pages is concatenated correctly.
        - Test with an empty/corrupt PDF (bytes): verify graceful error handling or empty string return.
        - Test with PDF containing no text (e.g., image-only PDF, assuming no OCR here): verify empty string or appropriate handling.
        - (Mock `pypdfium2.PdfDocument` for some error case simulations if direct PDF byte testing is hard for specific errors).
    -   `chunk_text_by_paragraph()`:
        - Test with text containing multiple double newlines: verify correct paragraph splitting.
        - Test with text having no double newlines: verify it returns a single chunk (or as per defined behavior).
        - Test with leading/trailing whitespace in paragraphs: verify stripping.
        - Test with empty input text: verify empty list or appropriate handling.
-   **`document_service.py`**:
    -   `create_document_and_chunks()`:
        - Mock `db.Session` and `extraction_service` functions.
        - Test new document creation: verify `Document` and `DocumentChunk` objects are correctly formed and added to session.
        - Test existing document (by hash): verify old chunks are deleted and new ones added.
        - Test correct `chunk_order` assignment.
        - Test handling of `original_file_name` update for existing document.
-   **`models/document.py`** (if any custom logic added beyond declarative definitions):
    - Test model-specific methods or properties.
-   **`core/config.py` & `core/database.py`**:
    - Unit tests for any utility functions if present; primarily these are configuration setup.

#### 2.1.2. Integration Tests (Endpoint: `POST /processing/process-pdf`)

-   **Test Setup**: Requires a running instance of `pdf_processor_service` and a (test) database if not fully mocking the DB.
-   **Test Cases**:
    -   **Valid PDF Upload**:
        - Upload a valid PDF file.
        - Assert HTTP 200 OK status.
        - Assert response body matches `DocumentResponse` schema.
        - Verify `Document` and `DocumentChunk` records are correctly created in the database (check content, hash, filename, chunk order, and count).
    -   **Duplicate PDF Upload (by content hash)**:
        - Upload the same PDF again.
        - Assert HTTP 200 OK.
        - Verify that the existing `Document` record is used/updated, old chunks are removed, and new chunks are stored. (Confirm `updated_at` changes for Document, and chunks are correct).
    -   **Invalid File Type**:
        - Upload a non-PDF file (e.g., .txt, .jpg).
        - Assert HTTP 400 Bad Request and specific error message.
    -   **Empty File Upload**:
        - Upload an empty file.
        - Assert HTTP 400 Bad Request and specific error message.
    -   **Corrupted PDF Upload**:
        - Upload a corrupted/malformed PDF.
        - Assert HTTP 500 Internal Server Error or appropriate error (e.g., 422 if `pypdfium2` fails gracefully and error is caught) and error message.
    -   **Large PDF Upload (if performance testing is in scope later)**: Monitor processing time and resource usage.

### 2.2. Main API Backend (Gateway)

#### 2.2.1. Integration Tests (Endpoint: `POST /api/v1/documents/upload-and-process`)

-   **Test Setup**: Requires a running instance of the main API. The `pdf_processor_service` will be mocked using `httpx.MockTransport` or by patching `httpx.AsyncClient`.
-   **Test Cases**:
    -   **Successful PDF Upload and Processing**:
        - Mock successful response (200 OK, valid JSON) from `pdf_processor_service`.
        - Send a valid PDF file to the gateway endpoint with authentication.
        - Assert HTTP 200 OK from gateway.
        - Assert response body from gateway matches the mocked response from microservice.
    -   **Authenticated Access**:
        - Attempt to access endpoint without authentication token.
        - Assert HTTP 401 Unauthorized (or 403 Forbidden depending on setup).
    -   **Invalid File Type (Gateway Level)**:
        - Upload a non-PDF file.
        - Assert HTTP 400 Bad Request from gateway (validating its own check).
    -   **Microservice Error Forwarding (e.g., 400, 422, 500 from `pdf_processor_service`)**:
        - Mock `pdf_processor_service` returning a specific error status code and JSON body.
        - Call gateway endpoint.
        - Assert that gateway forwards the same status code and error details.
    -   **Microservice Connection Error/Timeout**:
        - Mock `httpx.RequestError` (e.g., `ConnectError`, `TimeoutException`).
        - Call gateway endpoint.
        - Assert HTTP 503 Service Unavailable or appropriate error.

## 3. Test Environment and Tools

-   **Unit Tests**: `pytest`, `pytest-mock`, `pytest-asyncio`.
-   **Integration Tests (`pdf_processor_service`)**: `pytest`, `httpx` (for `TestClient`), potentially a test database instance or SQLAlchemy mocking.
-   **Integration Tests (Main API Gateway)**: `pytest`, `FastAPI TestClient`, `httpx.MockTransport`.
-   **Database**: PostgreSQL (test instance or Dockerized for CI/local testing).
-   **CI/CD**: (To be defined) Tests should be runnable in a CI environment.

## 4. Test Data Requirements

-   Sample valid PDF files (single page, multi-page, varying content).
-   Sample empty PDF file.
-   Sample corrupted/malformed PDF file.
-   Sample non-PDF files (e.g., .txt, .jpg, .png).
-   Sample PDF with only images (no extractable text).

## 5. Test Execution Strategy

1.  Develop and run unit tests for `pdf_processor_service` components first.
2.  Develop and run integration tests for the `pdf_processor_service` endpoint.
3.  Develop and run integration tests for the main API gateway endpoint.
4.  (Future) Develop and execute E2E tests for the entire pipeline.

## 6. Success Criteria

-   All planned unit tests pass.
-   All planned integration tests pass.
-   Code coverage targets met (e.g., >80% for new code in `pdf_processor_service` and gateway logic).

## 7. Risks and Mitigations

-   **Environment Setup for Integration Tests**: Setting up a consistent test DB and microservice instances can be complex.
    -   *Mitigation*: Use Docker for test dependencies; heavily mock external services for gateway tests.
-   **PDF Variety**: Real-world PDFs can be complex and varied.
    -   *Mitigation*: Use a diverse set of test PDFs. Initial focus on common PDF structures.
-   **Timeout issues during testing (as seen with Vitest previously)**: Python test runners might also face issues in constrained environments.
    -   *Mitigation*: Optimize tests, run in targeted batches, investigate environment if issues persist.
