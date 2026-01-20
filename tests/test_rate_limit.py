"""Tests for advanced rate limiting"""

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_register_rate_limit(client: AsyncClient):
    """Test rate limiting on register endpoint"""
    # Use a unique suffix to avoid 400 Bad Request
    import random
    suffix = random.randint(1000, 9999)

    triggered = False
    for i in range(10):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": f"rate{suffix}{i}@example.com",
                "username": f"rate{suffix}{i}",
                "password": "Password123!",
            }
        )
        if response.status_code == 429:
            triggered = True
            break

    assert triggered, "Rate limit (429) was never triggered"

@pytest.mark.asyncio
async def test_authenticated_user_rate_limit_headers(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test that authenticated users get rate limit headers"""
    response = await client.get("/api/v1/users/me", headers=normal_user_token_headers)
    assert response.status_code == 200
    # Headers added by slowapi
    assert "x-ratelimit-limit" in response.headers
    assert "x-ratelimit-remaining" in response.headers

@pytest.mark.asyncio
async def test_premium_user_rate_limit_higher(client: AsyncClient, db_session, normal_user_token_headers: dict[str, str]):
    """Test that premium users have higher rate limits"""
    from sqlalchemy import select

    from app.models.user import User

    # 1. Check normal limit first
    response = await client.get("/api/v1/users/me", headers=normal_user_token_headers)
    normal_limit = int(response.headers.get("x-ratelimit-limit", 0))

    # 2. Upgrade current user to premium
    # We need to use the email from the fixture. conftest.py uses "normal@example.com"
    result = await db_session.execute(select(User).where(User.email == "normal@example.com"))
    user = result.scalar_one()
    user.is_premium = True
    await db_session.commit()

    # 3. Check premium limit
    response = await client.get("/api/v1/users/me", headers=normal_user_token_headers)
    premium_limit = int(response.headers.get("x-ratelimit-limit", 0))

    assert premium_limit == normal_limit * 2
    assert premium_limit == settings.RATE_LIMIT_PER_MINUTE * 2
