# backend/tests/test_health.py
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the correct application root directory (/app/app) to the Python path
# Path(__file__).parent is /app/app/tests
# Path(__file__).parent.parent is /app/app
app_root_dir = str(Path(__file__).parent.parent)
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

# Now imports should work relative to the app root (/app/app)
from main import app
from core.config import settings

# Create a TestClient instance
client = TestClient(app)

def test_health_check_v1():
    """
    Test the v1 health check endpoint: /api/health/v1/health
    """
    health_url = f"{settings.API_PREFIX}/health/v1/health"
    response = client.get(health_url)
    assert response.status_code == 200
    expected_json = {"status": "ok", "message": "API health module v1 is active"}
    assert response.json() == expected_json

def test_read_root():
    """
    Test the root endpoint: /
    """
    response = client.get("/")
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert "environment" in response_data
    assert response_data["environment"] == settings.ENVIRONMENT
    assert response_data["api_base_prefix"] == settings.API_PREFIX