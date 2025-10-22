from fastapi.testclient import TestClient
from typing import Final
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from main import app
import random
from httpx import ASGITransport, AsyncClient
import pytest
from tests.integration.helper import create_and_login_user_with_role_super_adm

client: Final[TestClient] = TestClient(app)

@pytest.mark.asyncio
async def test_exists_by_email():
    email = "user9999999999@example.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/auth/{email}/exists/email")
    
    data = response.json()
    assert response.status_code == 200
    
    assert data['body'] == False
    assert data['code'] == 200
    assert data['version'] == 1
    assert data['path'] is None

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
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        dto_login = LoginDTO(email=user_data.dto.email, password=user_data.dto.password)
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
    user_data = await create_and_login_user_with_role_super_adm()

    assert user_data.tokens.refresh_token is not None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_get = await ac.get(f"/api/v1/auth/{user_data.tokens.refresh_token}")

    assert response_get.status_code == 200

    data_get = response_get.json()

    assert data_get['code'] == 200
    assert data_get['message'] == "New Tokens sent"
    assert data_get['status'] == True
    assert data_get['version'] == 1
    assert data_get['path'] is None
    assert data_get['body']['token'] is not None
    assert data_get['body']['refresh_token'] is not None