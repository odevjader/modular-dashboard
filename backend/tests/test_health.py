# backend/tests/test_health.py
from fastapi.testclient import TestClient
# Add path manipulation to help pytest find the 'app' module
# This assumes pytest is run from the 'backend' directory
import sys
from pathlib import Path
# Add the 'backend/app' directory to the system path
# Path(__file__).parent gives 'backend/tests'
# .parent gives 'backend'
# / "app" gives 'backend/app'
app_dir = str(Path(__file__).parent.parent / "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Now import the app and settings
# If VS Code shows import errors, they might resolve when running pytest
from main import app # Import the app instance from app/main.py
from core.config import settings # Import settings from app/core/config.py

# Create a TestClient instance
client = TestClient(app)

def test_health_check_v1():
    """
    Test the v1 health check endpoint: /api/health/v1/health
    """
    health_url = f"{settings.API_PREFIX}/health/v1/health"
    response = client.get(health_url)

    # Check status code is 200 OK
    assert response.status_code == 200

    # Check the response body matches the expected JSON
    expected_json = {"status": "ok", "message": "API health module v1 is active"}
    assert response.json() == expected_json

def test_read_root():
    """
    Test the root endpoint: /
    """
    response = client.get("/")

    # Check status code is 200 OK
    assert response.status_code == 200

    # Check some basic keys and values in the response
    response_data = response.json()
    assert "message" in response_data
    assert "environment" in response_data
    assert response_data["environment"] == settings.ENVIRONMENT
    assert response_data["api_base_prefix"] == settings.API_PREFIX