import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_v2_example_endpoint(client: AsyncClient):
    """Test that API v2 example endpoint works"""
    response = await client.get("/api/v2/example/example")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v2"
    assert data["message"] == "Hello from API v2!"


@pytest.mark.asyncio
async def test_v1_still_works(client: AsyncClient):
    """Regression test: Ensure API v1 still operates correctly"""
    response = await client.get("/health")
    # Health endpoint might return 200 OK
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
