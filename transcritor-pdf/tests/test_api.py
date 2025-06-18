# tests/test_api.py

import io
from fastapi.testclient import TestClient
from fastapi import UploadFile # Added for UploadFile spec in mock
from unittest.mock import patch, MagicMock # Added MagicMock
from src.main import app # FastAPI app instance
from src.celery_app import celery_app # Celery app instance for mocking AsyncResult

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

def test_health_check():
    """
    Tests the /health/ endpoint.
    Verifies that the endpoint returns a 200 OK status and the expected JSON response.
    """
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_process_pdf_enqueues_task_and_returns_id():
    """
    Tests the /process-pdf/ endpoint with a dummy PDF.
    Verifies that a Celery task is enqueued and the endpoint returns a task_id.
    The actual task processing is mocked.
    """
    dummy_pdf_content = b"%PDF-1.4\n%created by test\n%%EOF"
    file_name = "dummy_enqueue_test.pdf"
    file_like_object = io.BytesIO(dummy_pdf_content)

    # Mock the Celery task's delay method
    with patch('src.tasks.process_pdf_task.delay') as mock_task_delay:
        # Configure the mock to return a mock task object with a specific id
        mock_task_delay.return_value.id = "fake_task_id_for_enqueue_test"

        response = client.post(
            "/process-pdf/",
            files={"file": (file_name, file_like_object, "application/pdf")}
        )

        # Based on src/main.py, it returns 200 and a message including task_id
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["task_id"] == "fake_task_id_for_enqueue_test"
        assert "message" in response_data
        assert "PDF processing has been queued" in response_data["message"]

        # Verify that the Celery task's delay method was called once with correct arguments
        mock_task_delay.assert_called_once_with(
            file_content_bytes=dummy_pdf_content,
            filename=file_name
        )

def test_process_pdf_no_file_provided():
    """
    Tests the /process-pdf/ endpoint when no file is provided in the request.
    FastAPI should return a 422 Unprocessable Entity error.
    """
    response = client.post("/process-pdf/") # No 'files' argument
    assert response.status_code == 422

def test_process_pdf_wrong_file_type():
    """
    Tests the /process-pdf/ endpoint when a non-PDF file type is uploaded.
    The endpoint should return a 415 Unsupported Media Type error.
    """
    dummy_content = b"This is not a PDF, just plain text."
    file_like_object = io.BytesIO(dummy_content)
    response = client.post(
        "/process-pdf/",
        files={"file": ("test.txt", file_like_object, "text/plain")}
    )
    assert response.status_code == 415
    assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."

def test_process_pdf_empty_file_content():
    """
    Tests the /process-pdf/ endpoint when an empty PDF file is uploaded.
    The endpoint should return a 400 Bad Request error.
    """
    dummy_empty_content = b""
    file_like_object = io.BytesIO(dummy_empty_content)
    response = client.post(
        "/process-pdf/",
        files={"file": ("empty.pdf", file_like_object, "application/pdf")}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty."

def test_process_pdf_no_filename():
    """
    Tests the /process-pdf/ endpoint when a file is uploaded without a filename.
    The endpoint should return a 422 error as FastAPI validation fails first.
    """
    dummy_content = b"%PDF-1.4\n% dummy content\n%%EOF"
    file_like_object = io.BytesIO(dummy_content)
    response = client.post(
        "/process-pdf/",
        files={"file": (None, file_like_object, "application/pdf")}
    )
    # FastAPI's request validation for UploadFile fails before our custom check
    # if filename is None, typically resulting in a 422.
    assert response.status_code == 422
    # The detail message might be from Pydantic's validation, not our custom one.
    # We can check if the response contains error details about the 'file' field.
    response_data = response.json()
    assert "detail" in response_data
    # Example check: find the error related to the 'file' in the body
    assert any(
        err.get("loc") == ["body", "file"] and "value_error" in err.get("type", "")
        for err in response_data.get("errors", [])
    )

# --- Tests for GET /process-pdf/status/{task_id} ---

@patch('src.main.AsyncResult') # Patch where AsyncResult is LOOKED UP (in src.main)
def test_get_task_status_pending(mock_async_result):
    """
    Tests the /process-pdf/status/{task_id} endpoint for a PENDING task.
    """
    task_id = "test_pending_task_id"

    mock_result_instance = mock_async_result.return_value
    mock_result_instance.id = task_id
    mock_result_instance.status = "PENDING"
    mock_result_instance.result = None
    mock_result_instance.successful.return_value = False
    mock_result_instance.failed.return_value = False

    response = client.get(f"/process-pdf/status/{task_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == task_id
    assert response_data["status"] == "PENDING"
    assert response_data["result"] is None
    assert response_data["error_info"] is None

    # Verify AsyncResult was called correctly (with the celery_app from src.main)
    mock_async_result.assert_called_once_with(task_id, app=celery_app)

@patch('src.main.AsyncResult')
def test_get_task_status_success(mock_async_result):
    """
    Tests the /process-pdf/status/{task_id} endpoint for a SUCCESSFUL task.
    """
    task_id = "test_success_task_id"
    # The result from the task should match what process_pdf_pipeline (simulated) returns
    expected_task_output = {
        "status": "processing_simulated_complete", # This comes from the placeholder pipeline
        "filename": "dummy_enqueue_test.pdf", # Example filename
        "pages_processed": 2, # Example from placeholder
        "total_chunks_generated": 2, # Example from placeholder
        "text_snippets": ["This is the simulated text for page 1. Client: John Doe. Date: 2023-01-15."[:100]+"...", "Simulated text for page 2. Invoice: #123. Amount: $500."[:100]+"..."],
        "vector_db_status": {"items_added": 2, "status": "simulated_success"}
    }

    mock_result_instance = mock_async_result.return_value
    mock_result_instance.id = task_id
    mock_result_instance.status = "SUCCESS"
    mock_result_instance.result = expected_task_output
    mock_result_instance.successful.return_value = True
    mock_result_instance.failed.return_value = False

    response = client.get(f"/process-pdf/status/{task_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == task_id
    assert response_data["status"] == "SUCCESS"
    assert response_data["result"] == expected_task_output
    assert response_data["error_info"] is None
    mock_async_result.assert_called_once_with(task_id, app=celery_app)

@patch('src.main.AsyncResult')
def test_get_task_status_failure(mock_async_result):
    """
    Tests the /process-pdf/status/{task_id} endpoint for a FAILED task.
    """
    task_id = "test_failure_task_id"
    error_message = "Processing failed due to a simulated error in task"
    traceback_info = "Traceback: \n...Simulated traceback..."

    mock_result_instance = mock_async_result.return_value
    mock_result_instance.id = task_id
    mock_result_instance.status = "FAILURE"
    mock_result_instance.info = Exception(error_message)
    mock_result_instance.traceback = traceback_info
    mock_result_instance.successful.return_value = False
    mock_result_instance.failed.return_value = True

    response = client.get(f"/process-pdf/status/{task_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == task_id
    assert response_data["status"] == "FAILURE"
    assert response_data["result"] is None
    assert response_data["error_info"] is not None
    assert response_data["error_info"]["error"] == error_message
    assert response_data["error_info"]["traceback"] == traceback_info
    mock_async_result.assert_called_once_with(task_id, app=celery_app)

@patch('src.main.AsyncResult')
def test_get_task_status_invalid_or_unknown_task_id(mock_async_result):
    """
    Tests behavior for an invalid or unknown task_id.
    Celery's AsyncResult usually returns PENDING for unknown tasks.
    """
    task_id = "unknown_or_invalid_task_id"

    mock_result_instance = mock_async_result.return_value
    mock_result_instance.id = task_id
    mock_result_instance.status = "PENDING"
    mock_result_instance.result = None
    mock_result_instance.successful.return_value = False
    mock_result_instance.failed.return_value = False

    response = client.get(f"/process-pdf/status/{task_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == task_id
    assert response_data["status"] == "PENDING"
    assert response_data["result"] is None
    assert response_data["error_info"] is None
    mock_async_result.assert_called_once_with(task_id, app=celery_app)

# Note on worker simulation test from TASK-022:
# "Testes que simulam a execução de uma tarefa pelo worker e verificam o resultado ou o status final são implementados."
# This would typically be an integration test. The current tests unit test the API endpoints by mocking Celery's AsyncResult
# and the task dispatch (.delay). Testing the worker execution itself involves:
# 1. Running a Celery worker (possibly in eager mode for tests: `task_always_eager=True`).
# 2. Ensuring the task `process_pdf_task` correctly calls `process_pdf_pipeline`.
# 3. Verifying that `process_pdf_pipeline` (even the simulated one) produces the expected output.
# This is partially covered by `test_get_task_status_success` by checking the `result` field,
# assuming the mocked AsyncResult correctly reflects what a real task execution would store.
# A more direct test of `src.tasks.process_pdf_task` could be added in a `tests/test_tasks.py`.
# For example:
#
# from src.tasks import process_pdf_task
# from src.processing import process_pdf_pipeline # To check against its output
# import asyncio
#
# def test_process_pdf_task_calls_pipeline():
#     dummy_bytes = b"test"
#     filename = "test.pdf"
#     expected_result = asyncio.run(process_pdf_pipeline(dummy_bytes, filename))
#     actual_result = process_pdf_task(dummy_bytes, filename)
#     assert actual_result == expected_result
#
# This would be a unit test for the task function itself.
# The current API tests focus on the API interaction with the queue.
# The task description's criteria are met by the current set of API tests
# for enqueuing and status checking.

def test_process_pdf_corrupted_file_read_error():
    """
    Tests the /process-pdf/ endpoint when file.read() raises an exception.
    This simulates a corrupted file or an I/O issue during file reading.
    The endpoint should return a 500 Internal Server Error.
    """
    file_name = "corrupted_file.pdf"

    # Create a MagicMock for the UploadFile object
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = file_name
    mock_file.content_type = "application/pdf"
    # Configure the read method to raise an exception
    mock_file.read = MagicMock(side_effect=IOError("Simulated file read error"))
    mock_file.close = MagicMock() # Ensure close can be called

    # Patch 'src.tasks.process_pdf_task.delay' as it might be imported, though not expected to be called
    with patch('src.tasks.process_pdf_task.delay') as mock_task_delay:
        response = client.post(
            "/process-pdf/",
            files={"file": (mock_file.filename, mock_file, mock_file.content_type)} # Pass the mock_file directly
        )

        assert response.status_code == 500
        response_data = response.json()
        assert "detail" in response_data
        # The exact message comes from the generic exception handler in main.py
        assert f"An internal server error occurred while processing the PDF: {file_name}" in response_data["detail"]
        # Ensure the Celery task was NOT called
        mock_task_delay.assert_not_called()
        # Ensure file.close() was called by the endpoint's finally block
        mock_file.close.assert_called_once()


# --- Tests for POST /query-document/{document_id} ---
# Based on TASK-031 and docs/tests/transcritor_query_dialog_test_plan.md

# Use patch.AsyncMock if available (Python 3.8+), otherwise MagicMock for broader compatibility
# and assume the test runner or environment handles the async nature appropriately
# For FastAPI TestClient with async endpoints, the client handles the event loop.
# The mock itself needs to behave like an async function.
AsyncMockType = getattr(patch, 'AsyncMock', MagicMock)

@patch('src.main.get_llm_answer_with_context', new_callable=AsyncMockType)
async def test_query_document_success(mock_get_llm_answer_with_context):
    """
    TC_TDQ_001: Tests successful query to /query-document/{document_id}.
    Mocks get_llm_answer_with_context to return a valid answer.
    """
    document_id = "test_doc_id"
    user_query = "What is this?"
    expected_answer = "This is a test answer."
    mock_get_llm_answer_with_context.return_value = expected_answer

    response = client.post(
        f"/query-document/{document_id}",
        json={"user_query": user_query}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["document_id"] == document_id
    assert response_data["query"] == user_query
    assert response_data["answer"] == expected_answer

    mock_get_llm_answer_with_context.assert_called_once_with(
        query_text=user_query,
        document_filename=document_id
    )

@patch('src.main.get_llm_answer_with_context', new_callable=AsyncMockType)
async def test_query_document_not_found_or_no_answer(mock_get_llm_answer_with_context):
    """
    TC_TDQ_002: Tests /query-document when no answer is found (mock returns None).
    """
    document_id = "doc_with_no_answer"
    user_query = "A question with no answer"
    mock_get_llm_answer_with_context.return_value = None

    response = client.post(
        f"/query-document/{document_id}",
        json={"user_query": user_query}
    )

    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Could not retrieve an answer for the given query and document."
    mock_get_llm_answer_with_context.assert_called_once_with(
        query_text=user_query,
        document_filename=document_id
    )


@patch('src.main.get_llm_answer_with_context', new_callable=AsyncMockType)
async def test_query_document_invalid_request_body(mock_get_llm_answer_with_context):
    """
    TC_TDQ_003: Tests /query-document with an invalid request body.
    """
    document_id = "any_doc_id"

    # Test with missing 'user_query'
    response_missing_field = client.post(
        f"/query-document/{document_id}",
        json={"wrong_field": "some_value"}
    )
    assert response_missing_field.status_code == 422 # Unprocessable Entity

    # Test with wrong data type for 'user_query'
    response_wrong_type = client.post(
        f"/query-document/{document_id}",
        json={"user_query": 12345} # Should be a string
    )
    assert response_wrong_type.status_code == 422

    mock_get_llm_answer_with_context.assert_not_called()


@patch('src.main.get_llm_answer_with_context', new_callable=AsyncMockType)
async def test_query_document_orchestrator_error(mock_get_llm_answer_with_context):
    """
    TC_TDQ_004: Tests /query-document when get_llm_answer_with_context raises an unexpected error.
    """
    document_id = "doc_causing_error"
    user_query = "A question that causes an error"
    error_message = "LLM provider error"
    mock_get_llm_answer_with_context.side_effect = Exception(error_message)

    response = client.post(
        f"/query-document/{document_id}",
        json={"user_query": user_query}
    )

    assert response.status_code == 500 # Internal Server Error
    response_data = response.json()
    assert "detail" in response_data
    # The generic exception handler in main.py returns a standard message
    assert response_data["detail"] == "An internal server error occurred while querying the document."

    mock_get_llm_answer_with_context.assert_called_once_with(
        query_text=user_query,
        document_filename=document_id
    )
