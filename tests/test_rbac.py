
import pytest
from httpx import AsyncClient
from app.models.user import UserRole
from app.core.security import create_access_token
from app.schemas.user import TokenResponse

@pytest.mark.asyncio
async def test_rbac_admin_can_list_users(client: AsyncClient):
    """Test that ADMIN role can list users"""
    # 1. Register a user
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin_test@example.com",
            "username": "adminuser_test",
            "password": "Admin123!@#",
            "role": UserRole.ADMIN
        },
    )
    if reg_response.status_code != 201:
        print(f"DEBUG: Registration failed: {reg_response.json()}")
    assert reg_response.status_code == 201

    # 2. Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "adminuser_test", "password": "Admin123!@#"},
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
            "email": "user_test@example.com",
            "username": "normaluser_test",
            "password": "User123!@#",
            "role": UserRole.USER
        },
    )
    assert reg_response.status_code == 201, f"Reg failed: {reg_response.json()}"
    
    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "normaluser_test", "password": "User123!@#"},
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
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
            "email": "mod_test@example.com",
            "username": "moduser_test",
            "password": "Mod123!@#",
            "role": UserRole.MODERATOR
        },
    )
    assert reg_response.status_code == 201

    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "moduser_test", "password": "Mod123!@#"},
    )
    token = login_response.json()["data"]["access_token"]
    
    # 3. Try access
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["success"] is True
