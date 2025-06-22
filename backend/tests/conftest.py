import pytest
import os

@pytest.fixture(scope="function", autouse=True) # Changed to function scope
def set_test_environment_variables(monkeypatch): # Use standard monkeypatch fixture
    """
    Set environment variables for each test function.
    """
    monkeypatch.setenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://testuser:testpass@testhost:5432/testdb")
    # Add any other critical environment variables that Settings expects and are not in .env.example or are needed for tests
    monkeypatch.setenv("POSTGRES_USER", "testuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
    monkeypatch.setenv("POSTGRES_DB", "testdb")
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    # PDF_PROCESSOR_SERVICE_URL is removed as the service is deprecated
    # monkeypatch.setenv("PDF_PROCESSOR_SERVICE_URL", "http://mock-pdf-processor:8000")
