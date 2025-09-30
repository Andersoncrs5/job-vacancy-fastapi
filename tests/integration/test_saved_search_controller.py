from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, create_saved_search
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from app.schemas.saved_search_schemas import *
from app.schemas.saved_search_schemas import CreateSavedSearchDTO

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/saved-search'



@pytest.mark.asyncio
async def test_get_saved_search():
    user_data = await create_and_login_user()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{saved_search_data.id}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body']['id'] == saved_search_data.id
    assert data['body']['user_id'] == saved_search_data.user_id
    assert data['body']['name'] == saved_search_data.name

@pytest.mark.asyncio
async def test_create_saved_search():
    user_data = await create_and_login_user()

    dto = CreateSavedSearchDTO(
        name = "any query",
        query = dict({"name__ilike": "any"}),
        description = None,
        is_public = True,
        last_executed_at = None,
        notifications_enabled = False
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['user_id'] == user_data.out.id
    assert data['body']['name'] == dto.name