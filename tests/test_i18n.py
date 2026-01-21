import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_localization_default_language(client: AsyncClient):
    """Test that default language (English) is used when no header is present."""
    response = await client.get("/api/v2/example/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello"
    assert data["sub_message"] == "Welcome to the API"
    assert response.headers["Content-Language"] == "en"


@pytest.mark.asyncio
async def test_localization_turkish(client: AsyncClient):
    """Test that Turkish language is used when Accept-Language is 'tr'."""
    headers = {"Accept-Language": "tr"}
    response = await client.get("/api/v2/example/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Merhaba"
    assert data["sub_message"] == "API'ye hoşgeldiniz"
    assert response.headers["Content-Language"] == "tr"


@pytest.mark.asyncio
async def test_localization_fallback(client: AsyncClient):
    """Test that it falls back to default language for unsupported languages."""
    headers = {"Accept-Language": "fr"}
    response = await client.get("/api/v2/example/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello"
    assert response.headers["Content-Language"] == "en"


@pytest.mark.asyncio
async def test_localization_complex_header(client: AsyncClient):
    """Test parsing of complex Accept-Language headers."""
    # Preference: Turkish, then English
    headers = {"Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"}
    response = await client.get("/api/v2/example/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Merhaba"
    assert response.headers["Content-Language"] == "tr"


@pytest.mark.asyncio
async def test_localization_error_handling(client: AsyncClient):
    """Test that error messages are localized."""
    # Test 404 in Turkish
    headers = {"Accept-Language": "tr"}
    response = await client.get("/api/v2/non-existent-endpoint", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Kaynak bulunamadı"

    # Test 404 in English (default)
    response = await client.get("/api/v2/non-existent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Resource not found"
