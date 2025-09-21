from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

@pytest.mark.asyncio
async def test_create_category():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    data = response.json()

    assert data['code'] == 201
    assert data['message'] == 'Category created with successfully'
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None

    assert data['body']


