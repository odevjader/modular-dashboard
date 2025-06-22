# backend/app/tests/conftest.py
import pytest
import os
from unittest.mock import patch

@pytest.fixture(scope="session") # Removed autouse=True
def set_test_environment_variables_session_auto():
    """
    Sets default environment variables for the entire test session.
    This should be explicitly depended upon by fixtures that need these env vars set.
    """
    test_env_vars = {
        "POSTGRES_USER": "testsqliteuser", # Not strictly needed for SQLite in-memory
        "POSTGRES_PASSWORD": "testsqlitepassword", # Not strictly needed
        "POSTGRES_DB": "testsqlitedb", # Not strictly needed
        "DATABASE_URL": "sqlite+aiosqlite:///:memory:", # Sync version for Alembic/etc. if needed
        "ASYNC_DATABASE_URL": "sqlite+aiosqlite:///:memory:", # Async version for app
        "SECRET_KEY": "testsecretkey_sqlite",
        "ALGORITHM": "HS256_sqlite",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "34", # Changed to ensure it's different from a real value
        "GOOGLE_API_KEY": "testapikey_auto",
        "GEMINI_MODEL_NAME": "gemini-test-model-auto",
        "PDF_PROCESSOR_SERVICE_URL": "http://mock-pdf-processor-service-auto",
        "ENVIRONMENT": "test_auto"
    }
    # Patch os.environ BEFORE any critical imports happen (like app.core.config trying to load Settings)
    # This autouse=True, scope="session" fixture attempts to set them early.
    with patch.dict(os.environ, test_env_vars, clear=False) as patched_env:
        # No longer trying to manipulate app.core.config._settings_instance here directly,
        # as the timing is problematic during pytest collection phase.
        # The dependency_override approach in the test file's client fixture is more reliable.
        yield patched_env

@pytest.fixture(scope="session")
def event_loop():
    # Provides an event loop for session-scoped async fixtures
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_async_engine(set_test_environment_variables_session_auto):
    from sqlalchemy.ext.asyncio import create_async_engine
    from app.core.config import get_settings # Use get_settings to respect patched env

    settings = get_settings() # This will use the patched os.environ

    if "sqlite+aiosqlite" not in settings.ASYNC_DATABASE_URL:
        raise ValueError(
            "ASYNC_DATABASE_URL for tests must be 'sqlite+aiosqlite:///:memory:'"
        )

    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    yield engine # Return the engine directly
    await engine.dispose()

@pytest.fixture(scope="session", autouse=True)
async def create_test_tables(test_async_engine): # Depends on the test_async_engine
    from app.core.database import Base # Import Base from your models' base
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mock_db_session_fixture():
    from unittest.mock import AsyncMock, MagicMock # Import AsyncMock
    # from sqlalchemy.orm import Session # No longer needed for spec with AsyncMock
    from sqlalchemy.ext.asyncio import AsyncSession # Use AsyncSession for spec

    # db = MagicMock(spec=Session) # Original
    db = AsyncMock(spec=AsyncSession) # Make the session itself an AsyncMock

    # Mock the 'execute' method to be an AsyncMock as well, so it can be awaited
    # and also have return_value.scalars().all() chained.
    mock_execute_result = AsyncMock() # This will be the return value of db.execute()

    # Mock the chain .scalars().all()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [] # Default to returning an empty list for .all()

    mock_execute_result.scalars.return_value = mock_scalars

    db.execute = AsyncMock(return_value=mock_execute_result)

    # Add other common async mock configurations if needed
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock() # Typically not awaited, but can be AsyncMock if needed

    return db

@pytest.fixture
def mock_llm_fixture():
    from unittest.mock import AsyncMock, MagicMock
    llm = AsyncMock()
    ai_message_mock = MagicMock()
    ai_message_mock.content = "Quesito gerado mockado 1.\nQuesito gerado mockado 2."
    llm.ainvoke.return_value = ai_message_mock
    return llm

@pytest.fixture
def valid_token_header_fixture():
    # This should ideally generate or retrieve a real test token.
    # For now, a placeholder.
    # If your tests mock get_current_active_user, this might not be strictly necessary
    # unless middleware relies on it.
    return {"Authorization": "Bearer testtoken"}

# If you have a TestClient instance you use often, you can make it a fixture too.
# However, since app loading depends on env vars, it's often better to initialize it
# within tests or fixtures that run *after* env vars are patched.
# Example (if you ensure env vars are set before this runs):
# @pytest.fixture(scope="module")
# def test_app_client():
#     from fastapi.testclient import TestClient
#     from app.main import app # Assuming app is loaded after env vars are set
#     client = TestClient(app)
#     return client

# This fixture can be used to override the get_db dependency in endpoints
# @pytest.fixture
# def override_get_db(mock_db_session_fixture):
#     from app.main import app
#     from app.core.database import get_db
#     app.dependency_overrides[get_db] = lambda: mock_db_session_fixture
#     yield
#     app.dependency_overrides.pop(get_db, None)

# Note: The `autouse=True` for `set_test_environment_variables` ensures it runs for all tests.
# Individual test files can still further patch os.environ if a specific test needs a different value.
# The `clear=False` in patch.dict is important to avoid clearing other potentially set CI environment variables.
# However, for full isolation, `clear=True` might be preferred if you are sure no other env vars are needed.
# For this project, `clear=False` is safer initially.
