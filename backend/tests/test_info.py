# backend/tests/test_info.py
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add application root directory to path
app_root_dir = str(Path(__file__).parent.parent / "app")
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

# Import app and settings
from main import app
from core.config import settings

# Create Test Client
client = TestClient(app)

def test_get_system_status_v1():
    """
    Test the GET /api/info/v1/status endpoint.
    """
    status_url = f"{settings.API_PREFIX}/info/v1/status"
    response = client.get(status_url)

    # Check status code is 200 OK
    assert response.status_code == 200

    # Check response body structure and types
    data = response.json()
    assert "environment" in data
    assert data["environment"] == settings.ENVIRONMENT
    assert "project_name" in data
    assert data["project_name"] == settings.PROJECT_NAME
    assert "server_time_utc" in data
    # Basic check for datetime format (will be string in JSON)
    assert isinstance(data["server_time_utc"], str)
    assert "api_prefix" in data
    assert data["api_prefix"] == settings.API_PREFIX