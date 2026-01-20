"""Tests for advanced rate limiting"""

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_register_rate_limit(client: AsyncClient):
    """Test rate limiting on register endpoint"""
    import random
    suffix = random.randint(1000, 9999)

    triggered = False
    for i in range(12):
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

    assert triggered, f"Rate limit (429) was never triggered. Last status: {response.status_code}"

@pytest.mark.asyncio
async def test_authenticated_user_rate_limit_headers(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test that authenticated users get rate limit headers"""
    response = await client.get("/api/v1/users/me", headers=normal_user_token_headers)
    assert response.status_code == 200

    print(f"DEBUG Headers: {response.headers}")

    # Headers added by slowapi (case-insensitive in httpx)
    assert "x-ratelimit-limit" in response.headers or "ratelimit-limit" in response.headers
    assert "x-ratelimit-remaining" in response.headers or "ratelimit-remaining" in response.headers

@pytest.mark.asyncio
async def test_premium_user_rate_limit_higher(client: AsyncClient, db_session, normal_user_token_headers: dict[str, str]):
    """Test that premium users have higher rate limits"""
    from sqlalchemy import select

    from app.models.user import User

    # 1. Check normal limit first
    response = await client.get("/api/v1/users/me", headers=normal_user_token_headers)
    assert response.status_code == 200

    # Try different possible header names
    limit_header = response.headers.get("x-ratelimit-limit", response.headers.get("ratelimit-limit", "0"))
    if "," in limit_header:
        limit_header = limit_header.split(",")[0].strip()
    normal_limit = int(limit_header)

    assert normal_limit > 0, f"Rate limit headers missing. Headers: {response.headers}"
    assert normal_limit == settings.RATE_LIMIT_PER_MINUTE

    # 2. Upgrade current user to premium
    result = await db_session.execute(select(User).where(User.email == "normal@example.com"))
    user = result.scalar_one()
    user.is_premium = True
    await db_session.commit()

    # 3. Re-login to get a fresh token with is_premium=True claim
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "normaluser", "password": "Password123!"},
        headers={"X-Skip-Rate-Limit": "test-bypass-secret"}
    )
    premium_token = login_response.json()["data"]["access_token"]
    premium_headers = {"Authorization": f"Bearer {premium_token}"}

    # 4. Check premium limit
    response = await client.get("/api/v1/users/me", headers=premium_headers)
    limit_header = response.headers.get("x-ratelimit-limit", response.headers.get("ratelimit-limit", "0"))
    if "," in limit_header:
        limit_header = limit_header.split(",")[0].strip()
    premium_limit = int(limit_header)

    assert premium_limit == normal_limit * 2
    assert premium_limit == settings.RATE_LIMIT_PER_MINUTE * 2
