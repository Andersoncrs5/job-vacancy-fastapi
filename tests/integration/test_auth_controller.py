from fastapi.testclient import TestClient
from typing import Final
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from main import app
import random
from httpx import ASGITransport, AsyncClient
import pytest

client: Final[TestClient] = TestClient(app)

@pytest.mark.asyncio
async def test_register_user():
    num = random.randint(1000000, 10000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dict(dto))

    assert response.status_code == 201

@pytest.mark.anyio
async def test_register_and_login_user():
    num = random.randint(1000000, 10000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dict(dto))
    assert response.status_code == 201


    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        dto_login = LoginDTO(email=dto.email, password=dto.password)
        response = await ac.post("/api/v1/auth/login", json=dict(dto_login))
    assert response.status_code == 200

    data = response.json()

    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body']['token'] is not None
    assert data['body']['refresh_token'] is not None
    
@pytest.mark.anyio
async def test_refresh_token():
    num = random.randint(1000000, 10000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dict(dto))
    assert response.status_code == 201

    data = response.json()

    assert data['body']['refresh_token'] is not None

    refresh_token = str(data['body']['refresh_token'])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_get = await ac.get(f"/api/v1/auth/{refresh_token}")

    assert response_get.status_code == 200

    data_get = response_get.json()

    assert data_get['code'] == 200
    assert data_get['message'] == "New Tokens sended"
    assert data_get['status'] == True
    assert data_get['version'] == 1
    assert data_get['path'] is None
    assert data_get['body']['token'] is not None
    assert data_get['body']['refresh_token'] is not None