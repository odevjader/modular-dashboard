import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Adjust these imports based on your project structure
from app.core.database import async_engine, Base, get_db_contextmanager
from app.models.user import User
from app.models.enums import UserRole
from app.core.security import hash_password

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin@gmail.com" # Script will hash this

async def create_initial_admin_user():
    logger.info("Attempting to create initial admin user...")

    async with get_db_contextmanager() as db: # Use the context manager for session
        # Check if admin user already exists
        stmt = select(User).where(User.email == ADMIN_EMAIL)
        result = await db.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            logger.info(f"User with email {ADMIN_EMAIL} already exists. Role: {existing_user.role}. Active: {existing_user.is_active}")
            if existing_user.role != UserRole.ADMIN:
                logger.info(f"User {ADMIN_EMAIL} exists but is not an ADMIN. Updating role to ADMIN.")
                existing_user.role = UserRole.ADMIN
                db.add(existing_user)
                await db.commit()
                await db.refresh(existing_user)
                logger.info("User role updated to ADMIN.")
            if not existing_user.is_active:
                logger.info(f"User {ADMIN_EMAIL} exists but is not active. Activating user.")
                existing_user.is_active = True
                db.add(existing_user)
                await db.commit()
                await db.refresh(existing_user)
                logger.info("User activated.")
            return

        # If user does not exist, create new admin user
        logger.info(f"Creating new admin user: {ADMIN_EMAIL}")
        hashed_admin_password = hash_password(ADMIN_PASSWORD)

        new_admin_user = User(
            email=ADMIN_EMAIL,
            hashed_password=hashed_admin_password,
            role=UserRole.ADMIN,
            is_active=True
        )

        db.add(new_admin_user)
        await db.commit()
        await db.refresh(new_admin_user)
        logger.info(f"Admin user {ADMIN_EMAIL} created successfully.")

async def main():
    # This is optional, can be used to create tables if they don't exist
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    await create_initial_admin_user()

if __name__ == "__main__":
    logger.info("Running admin user creation script...")
    asyncio.run(main())
    logger.info("Script finished.")
