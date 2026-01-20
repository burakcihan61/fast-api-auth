"""Test configuration and fixtures"""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

# Use test database
TEST_DATABASE_URL = (
    settings.TEST_DATABASE_URL or "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp_test"
)

# Create async engine for testing
engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

# Create async session factory
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database session override"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import ASGITransport

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def normal_user_token_headers(
    client: AsyncClient, db_session: AsyncSession
) -> dict[str, str]:
    """Create a normal user and return authorization headers"""
    user_data = {
        "email": "normal@example.com",
        "username": "normaluser",
        "password": "Password123!",
        "full_name": "Normal User",
    }

    # Register with bypass header
    await client.post(
        "/api/v1/auth/register", json=user_data, headers={"X-Skip-Rate-Limit": "test-bypass-secret"}
    )

    # Login with bypass header
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user_data["username"], "password": user_data["password"]},
        headers={"X-Skip-Rate-Limit": "test-bypass-secret"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def superuser_token_headers(client: AsyncClient, db_session: AsyncSession) -> dict[str, str]:
    """Create a superuser and return authorization headers"""
    from app.core.security import get_password_hash
    from app.models.user import User

    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("Admin123!"),
        is_superuser=True,
    )
    db_session.add(user)
    await db_session.commit()

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin123!"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
