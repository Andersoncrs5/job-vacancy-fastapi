from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user, create_category
from main import app
from app.schemas.user_schemas import UserOUT, UpdateUserDTO
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

URL: Final[str] = "/api/v1/user"

@pytest.mark.asyncio
async def test_get_all_user():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(URL, headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

@pytest.mark.asyncio
async def test_update_user():
    user_data: Final = await create_and_login_user()

    dto = UpdateUserDTO(
        name = "user updated",
        password = None,
        bio = "bio updated",
        avatar_url = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put(URL, json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 200

    assert data['message'] == "User updated with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body']['bio'] == dto.bio
    assert data['body']['name'] == dto.name
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_delete_user():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(URL, headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data['code'] == 200
    assert data['message'] == "User deleted with successfully"
    assert data['status'] == True
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_get_user_by_email():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(URL + f"/{user_data.dto.email}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data['code'] == 200
    assert data['message'] == "User found with successfully"
    assert data['status'] == True
    assert data['body']['email'] == user_data.dto.email
    assert data['body']['name'] == user_data.dto.name
    assert data['version'] == 1
    assert data['path'] is None