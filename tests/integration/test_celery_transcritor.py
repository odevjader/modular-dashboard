import os
import time
from celery import Celery
from celery.result import AsyncResult

# Determine broker and backend URLs from environment variables or use defaults
BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
BACKEND_URL = os.getenv('CELERY_BACKEND_URL', 'redis://redis:6379/1')

# Initialize a Celery app instance for sending tasks
# This app instance is only for sending tasks, not for defining them here.
# The task definitions are in the worker's codebase.
client_app = Celery('client_app_for_tests', broker=BROKER_URL, backend=BACKEND_URL)
client_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=60 # Short expiry for test results
)

def test_transcritor_celery_health_check():
    task_name = "transcritor_pdf.tasks.health_check_task"
    print(f"Sending task: {task_name} to broker {BROKER_URL}")

    try:
        async_result = client_app.send_task(task_name)
        print(f"Task {task_name} sent. ID: {async_result.id}")

        timeout_seconds = 45  # Max wait time for the task
        start_time = time.time()
        result = None

        while time.time() - start_time < timeout_seconds:
            if async_result.ready():
                if async_result.successful():
                    result = async_result.get(timeout=5) # Short timeout for get once ready
                    print(f"Task {async_result.id} successful with result: {result}")
                elif async_result.failed():
                    print(f"Task {async_result.id} failed. Traceback: {async_result.traceback}")
                    raise Exception(f"Task {task_name} failed: {async_result.traceback}")
                break
            print(f"Waiting for task {async_result.id}, current state: {async_result.state}...")
            time.sleep(1)

        if not async_result.ready():
            print(f"Task {async_result.id} timed out after {timeout_seconds} seconds. State: {async_result.state}")
            raise TimeoutError(f"Task {task_name} did not complete within {timeout_seconds} seconds.")

        assert async_result.successful(), f"Task {task_name} did not succeed. State: {async_result.state}"
        assert result == "Celery is healthy!", f"Expected 'Celery is healthy!' but got '{result}'"
        print(f"Task {task_name} completed successfully with result: {result}")

    except Exception as e:
        print(f"An error occurred during Celery health check: {e}")
        raise

if __name__ == "__main__":
    print("Running Celery transcritor health check test...")
    try:
        test_transcritor_celery_health_check()
        print("Celery transcritor health check PASSED")
    except Exception as e:
        print(f"Celery transcritor health check FAILED: {e}")
        # Re-raise to ensure script exits with non-zero on failure for automation
        raise
