import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        "/api/auth/register",
        json={"email": "alice@example.com", "password": "strongpass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {"email": "bob@example.com", "password": "strongpass123"}
    await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={"email": "carol@example.com", "password": "strongpass123"},
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "carol@example.com", "password": "strongpass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={"email": "dave@example.com", "password": "strongpass123"},
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "dave@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
