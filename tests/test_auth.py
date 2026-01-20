"""Test authentication endpoints"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"
    assert data["data"]["username"] == "testuser"
    assert "hashed_password" not in data["data"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test123!@#",
    }

    # First registration
    await client.post("/api/v1/auth/register", json=user_data)

    # Second registration with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={**user_data, "username": "different"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login"""
    # Register user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#",
        },
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "Test123!@#"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password"""
    # Register user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#",
        },
    )

    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "WrongPassword123!"},
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """Test registration with weak password"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak",
        },
    )
    assert response.status_code == 422
