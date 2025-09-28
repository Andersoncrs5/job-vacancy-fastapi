from fastapi.testclient import TestClient
from typing import Final
from app.schemas.employee_enterprise_schemas import *
from tests.integration.helper import create_and_login_user, create_industry, create_enterprise
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/employee-enterprise'

@pytest.mark.asyncio
async def test_get_all_enterprise():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200