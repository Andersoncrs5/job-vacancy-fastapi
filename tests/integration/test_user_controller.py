from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user, create_category
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

URL: Final[str] = "/api/v1/user"

@pytest.mark.asyncio
async def delete():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(URL+"/me", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data['code'] == 200
    assert data['message'] == "User deleted with successfully"
    assert data['status'] == True
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def get_user():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(URL+"/me", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data['code'] == 200
    assert data['message'] == "User found with successfully"
    assert data['status'] == True
    assert data['body']['email'] == user_data.dto.email
    assert data['body']['name'] == user_data.dto.name
    assert data['version'] == 1
    assert data['path'] is None