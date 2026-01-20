
import pytest
from httpx import AsyncClient
from app.models.user import UserRole
from app.core.security import create_access_token
from app.schemas.user import TokenResponse

@pytest.mark.asyncio
async def test_rbac_admin_can_list_users(client: AsyncClient):
    """Test that ADMIN role can list users"""
    # Create an admin user directly in DB or use register + role update
    # For testing, we can register as normal and mock/assume role for token
    
    # 1. Register a user
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@example.com",
            "username": "adminuser",
            "password": "Admin123!@#",
            "role": UserRole.ADMIN
        },
    )
    if reg_response.status_code != 201:
        print(f"DEBUG: Registration failed: {reg_response.json()}")
    assert reg_response.status_code == 201
    admin_id = reg_response.json()["data"]["id"]

    # 2. Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "adminuser", "password": "Admin123!@#"},
    )
    token = login_response.json()["data"]["access_token"]
    
    # 3. Try to access users list
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_rbac_user_cannot_list_users(client: AsyncClient):
    """Test that standard USER role cannot list users"""
    # 1. Register a normal user
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "username": "normaluser",
            "password": "User123!@#",
            "role": UserRole.USER
        },
    )
    assert reg_response.status_code == 201

    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "normaluser", "password": "User123!@#"},
    )
    token = login_response.json()["data"]["access_token"]
    
    # 3. Try to access users list
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users", headers=headers)
    
    # Should be Forbidden (403)
    assert response.status_code == 403
    assert "not have enough permissions" in response.json()["detail"]

@pytest.mark.asyncio
async def test_rbac_moderator_can_list_users(client: AsyncClient):
    """Test that MODERATOR role can list users"""
    # 1. Register a moderator
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "mod@example.com",
            "username": "moduser",
            "password": "Mod123!@#",
            "role": UserRole.MODERATOR
        },
    )
    assert reg_response.status_code == 201

    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "moduser", "password": "Mod123!@#"},
    )
    token = login_response.json()["data"]["access_token"]
    
    # 3. Try access
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["success"] is True
