import pytest
from httpx import AsyncClient


async def get_auth_header(client: AsyncClient) -> dict:
    """Helper: register + login and return the auth header."""
    await client.post(
        "/api/auth/register",
        json={"email": "todouser@example.com", "password": "strongpass123"},
    )
    resp = await client.post(
        "/api/auth/login",
        json={"email": "todouser@example.com", "password": "strongpass123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    response = await client.post(
        "/api/todos/",
        json={"title": "Buy groceries", "priority": 2},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Buy groceries"


@pytest.mark.asyncio
async def test_list_todos(client: AsyncClient):
    headers = await get_auth_header(client)
    await client.post("/api/todos/", json={"title": "Task 1"}, headers=headers)
    await client.post("/api/todos/", json={"title": "Task 2"}, headers=headers)

    response = await client.get("/api/todos/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    create_resp = await client.post(
        "/api/todos/", json={"title": "Incomplete"}, headers=headers
    )
    todo_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/todos/{todo_id}",
        json={"is_completed": True},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    create_resp = await client.post(
        "/api/todos/", json={"title": "Delete me"}, headers=headers
    )
    todo_id = create_resp.json()["id"]

    response = await client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 204

    # Verify it's gone
    get_resp = await client.get(f"/api/todos/{todo_id}", headers=headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/todos/")
    assert response.status_code == 401
