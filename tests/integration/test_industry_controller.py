from fastapi.testclient import TestClient
from typing import Final
from app.schemas.industry_schemas import *
from tests.integration.helper import create_and_login_user, create_category
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/industry'

@pytest.mark.asyncio
async def test_create_industry():
    num: Final = random.randint(1000,10000000000000)
    user_data: Final = await create_and_login_user()

    dto: Final = CreateIndustryDTO(
        name = f"name {num}",
        description = None,
        icon_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data: Final = response.json()        

    assert data['message'] == "Industry created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert isinstance(data['body']['id'], int)
    assert data['body']['name'] == dto.name
    assert data['body']['description'] == dto.description
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['user_id'] is not None
    assert isinstance(data['body']['user_id'], int)
    assert data['body']['is_active'] == True