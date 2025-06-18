import httpx
from fastapi import UploadFile, HTTPException

# URL for the transcriber PDF service, expected to be running and accessible.
# The hostname "transcritor_pdf_service" should be resolvable by this service,
# typically in a containerized environment (e.g., Docker Compose).
TRANSCRIBER_SERVICE_URL = "http://transcritor_pdf_service:8002/process-pdf"

async def handle_file_upload(file: UploadFile, user_id: int):
    """
    Handles the file upload by sending it to the transcriber PDF service.

    Args:
        file: The UploadFile object received from the FastAPI request.
        user_id: The ID of the user uploading the file.

    Returns:
        A dictionary with a success message and data from the transcriber service.

    Raises:
        HTTPException: If there's an error during the process (e.g., connection issues,
                       error response from transcriber service, or other unexpected errors).
    """
    async with httpx.AsyncClient() as client:
        try:
            # Read file content into memory. For very large files, streaming might be preferred,
            # but that would require changes in how the client sends the file and how the
            # receiving service handles it (e.g., supporting chunked transfer encoding explicitly
            # for streaming if it doesn't already). `await file.read()` is common for now.
            file_content = await file.read()

            # Prepare the file data for the multipart/form-data request.
            # 'upload_file' is the field name the transcriber_pdf_service is expected to use for the file.
            # This needs to match the parameter name in the transcriber service's endpoint.
            files_data = {'upload_file': (file.filename, file_content, file.content_type)}

            # Prepare other form data, like user_id.
            form_data = {'user_id': str(user_id)}

            response = await client.post(
                TRANSCRIBER_SERVICE_URL,
                files=files_data,
                data=form_data,
                timeout=60.0  # Increased timeout to 60 seconds for potentially larger files/slower processing
            )

            # Raise an exception for 4xx (client errors) or 5xx (server errors) responses.
            response.raise_for_status()

            # Assuming the transcriber service returns a JSON response on success.
            transcriber_response = response.json()

            return {
                "message": "File successfully processed by transcriber.",
                "transcriber_data": transcriber_response,
                "original_filename": file.filename,
                "uploader_user_id": user_id
            }
        except httpx.HTTPStatusError as e:
            # Error response from the transcriber service (e.g., 400, 422, 500)
            # It's often good practice to not expose the exact error message from downstream services
            # directly to the client, as it might reveal internal implementation details.
            # Log the detailed error (e.g., e.response.text) for debugging on the server.
            # For this exercise, we'll forward a structured detail.
            error_detail = f"Error from transcriber service: Status {e.response.status_code}."
            # Consider logging e.response.text here for internal diagnostics
            # print(f"Transcriber service error: {e.response.text}") # Example logging
            raise HTTPException(
                status_code=e.response.status_code, # Or a generic 502/503 if you prefer to mask it
                detail=error_detail
            )
        except httpx.RequestError as e:
            # Network-related errors (e.g., connection refused, DNS resolution failure)
            # This indicates the transcriber service might be down or unreachable.
            # Log the detailed error for debugging.
            # print(f"RequestError connecting to transcriber: {str(e)}") # Example logging
            raise HTTPException(
                status_code=503, # Service Unavailable
                detail=f"Could not connect to transcriber service. Please try again later."
            )
        except Exception as e:
            # Catch-all for any other unexpected errors during the process.
            # This could be issues with file reading, an unexpected httpx error not caught above, etc.
            # Log the detailed error for debugging.
            # print(f"Unexpected error in handle_file_upload: {str(e)}") # Example logging
            raise HTTPException(
                status_code=500, # Internal Server Error
                detail="An unexpected error occurred while processing the file."
            )
        finally:
            # It's crucial to close the uploaded file to free up resources.
            await file.close()

# To keep the module clean, the example_service_function has been removed.
# If you need other service functions, define them here.
