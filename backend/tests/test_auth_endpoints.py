import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

# Assuming your FastAPI app instance is accessible for testing setup
# This might need adjustment based on your test setup structure
# For example, if you have a conftest.py that provides the app or client
from app.main import app # Or your FastAPI app instance
from app.core_modules.auth.v1 import schemas as auth_schemas
from app.models import user as user_model
from app.core.security import hash_password # For creating test users directly
from app.models.enums import UserRole

@pytest.fixture(scope="function") # function scope for db interactions
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

async def create_test_user_in_db(
    db: AsyncSession,
    email: str,
    password: str,
    role: UserRole = UserRole.USER,
    is_active: bool = True
) -> user_model.User:
    user = user_model.User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        is_active=is_active
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@pytest.mark.asyncio
async def test_create_user_by_admin(async_client: AsyncClient, db_session: AsyncSession): # Assuming db_session fixture
    # Create an admin user first to get an admin token
    # Ensure this email is unique for each test run or use a cleanup mechanism
    admin_email = "admin_create_test@example.com"
    admin_pass = "adminpass"

    # It's good practice to check if admin already exists if tests share DB without cleanup
    # For simplicity here, we assume it can be created or rely on unique emails per test function
    admin_user_query = await db_session.execute(
        user_model.User.__table__.select().where(user_model.User.email == admin_email)
    )
    if admin_user_query.first() is None:
        admin = await create_test_user_in_db(db_session, admin_email, admin_pass, UserRole.ADMIN)
    else: # If admin exists, perhaps fetch it or ensure it's active and has the right role
        admin = await db_session.get(user_model.User, admin_user_query.first().id) # Example fetch
        if not admin or admin.role != UserRole.ADMIN or not admin.is_active :
             # Fallback or raise error if existing admin is not suitable
             admin = await create_test_user_in_db(db_session, admin_email, admin_pass, UserRole.ADMIN, is_active=True)


    login_data = {"username": admin_email, "password": admin_pass}
    response = await async_client.post("/api/auth/v1/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    admin_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    new_user_data = {
        "email": "newuser_create_test@example.com", # Unique email
        "password": "newuserpass",
        "role": UserRole.USER.value, # Use enum value
        "is_active": True
    }
    response = await async_client.post("/api/auth/v1/admin/users", json=new_user_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    created_user = response.json()
    assert created_user["email"] == new_user_data["email"]
    assert created_user["role"] == new_user_data["role"] # Schema should return the value e.g. "user"
    assert created_user["is_active"] == new_user_data["is_active"]
    assert "id" in created_user

    # TODO: Add test for duplicate email (400)
    # response_duplicate = await async_client.post("/api/auth/v1/admin/users", json=new_user_data, headers=headers)
    # assert response_duplicate.status_code == status.HTTP_400_BAD_REQUEST

    # TODO: Add test for creation attempt by non-admin (403)
    # non_admin_user = await create_test_user_in_db(db_session, "nonadmin_create_test@example.com", "userpass", UserRole.USER)
    # login_non_admin_data = {"username": "nonadmin_create_test@example.com", "password": "userpass"}
    # response_non_admin_login = await async_client.post("/api/auth/v1/login", data=login_non_admin_data)
    # non_admin_token = response_non_admin_login.json()["access_token"]
    # headers_non_admin = {"Authorization": f"Bearer {non_admin_token}"}
    # response_non_admin_create = await async_client.post("/api/auth/v1/admin/users", json={"email": "another@example.com", "password": "pw"}, headers=headers_non_admin)
    # assert response_non_admin_create.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_list_users_by_admin_pagination(async_client: AsyncClient, db_session: AsyncSession):
    list_admin_email = "listadmin_pagination_test@example.com"
    list_admin_pass = "adminpass"

    # Similar check for admin user as in the previous test
    list_admin_user_query = await db_session.execute(
        user_model.User.__table__.select().where(user_model.User.email == list_admin_email)
    )
    if list_admin_user_query.first() is None:
        admin = await create_test_user_in_db(db_session, list_admin_email, list_admin_pass, UserRole.ADMIN)
    else:
        admin = await db_session.get(user_model.User, list_admin_user_query.first().id)
        if not admin or admin.role != UserRole.ADMIN or not admin.is_active :
             admin = await create_test_user_in_db(db_session, list_admin_email, list_admin_pass, UserRole.ADMIN, is_active=True)


    # Create a few users for pagination testing - ensure unique emails for test runs
    await create_test_user_in_db(db_session, "user1_pagination_test@example.com", "pass1")
    await create_test_user_in_db(db_session, "user2_pagination_test@example.com", "pass2")
    await create_test_user_in_db(db_session, "user3_pagination_test@example.com", "pass3")

    login_data = {"username": list_admin_email, "password": list_admin_pass}
    response = await async_client.post("/api/auth/v1/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    admin_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Test first page
    # To make total count predictable, one might count users before adding new ones,
    # or ensure a clean slate database for each test function/module.
    # For now, we assume at least these 3 + admin exist.
    initial_users_count_stmt = await db_session.execute(user_model.User.__table__.select().where(user_model.User.email.like('%_pagination_test@example.com')))
    # This counts only users created in this test, if emails are unique like this.
    # Total users created in this test (admin + 3 users) = 4.
    # If admin was pre-existing, then 3.
    # A more robust way is to query total count from DB before creating users if DB is not cleaned.

    response = await async_client.get("/api/auth/v1/admin/users?skip=0&limit=2", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    paginated_response = response.json()

    assert len(paginated_response["items"]) <= 2 # Can be less if total is less than limit
    # assert paginated_response["total"] >= 4 # At least admin + 3 users if created, could be more
    # A more precise total assertion would require knowing the full DB state or cleaning it.
    # For example, query total before this test, then assert total is previous_total + 4.
    assert paginated_response["page"] == 1
    assert paginated_response["size"] == len(paginated_response["items"]) # size should be actual items returned

    # TODO: Add more specific checks for content and other pages
    # e.g., get full list, then check if items on page 1 match first N of full list.
    # Then get page 2 (skip=2, limit=2) and check items.
    # TODO: Add test for listing attempt by non-admin (403)
    # TODO: Add test for invalid pagination params (e.g. limit > 100, negative skip)
```
