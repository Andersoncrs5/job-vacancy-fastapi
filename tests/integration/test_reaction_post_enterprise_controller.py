from typing import Final

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.configs.db.enums import ReactionTypeEnum
from app.schemas.reaction_post_enterprise_schemas import CreateReactionPostEnterpriseDTO
from main import app
from tests.integration.helper import create_and_login_user, create_category, create_post_enterprise, create_enterprise, \
    create_industry, create_reaction_post_enterprise

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/area/reaction-post-enterprise"

@pytest.mark.asyncio
async def test_toggle_post_enterprise_not_found():
    user_data = await create_and_login_user()

    dto = CreateReactionPostEnterpriseDTO(
        post_enterprise_id=999999,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Post not found"
    assert data["code"] == 404
    assert data["status"] is False
    assert data["body"] is None

@pytest.mark.asyncio
async def test_toggle_change_reaction_like_to_dislike_enterprise():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    await create_reaction_post_enterprise(
        post_data=post_data,
        reaction=ReactionTypeEnum.LIKE,
        user_data=user_data
    )

    dto = CreateReactionPostEnterpriseDTO(
        post_enterprise_id=post_data.id,
        reaction_type=ReactionTypeEnum.DISLIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Reaction updated with successfully"
    assert data["code"] == 200
    assert data["status"] is True
    assert data["body"] is None

@pytest.mark.asyncio
async def test_toggle_remove_reaction_like_enterprise():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    await create_reaction_post_enterprise(
        post_data=post_data,
        reaction=ReactionTypeEnum.LIKE,
        user_data=user_data
    )

    dto = CreateReactionPostEnterpriseDTO(
        post_enterprise_id=post_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Reaction removed with successfully"
    assert data["code"] == 200
    assert data["status"] is True
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_all_by_user_id():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    await create_reaction_post_enterprise(
        post_data=post_data,
        reaction=ReactionTypeEnum.LIKE,
        user_data=user_data
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert len(data["items"]) > 0

    react = data["items"][0]
    assert react["user_id"] == user_data.out.id
    assert react["post_enterprise_id"] == post_data.id
    assert react["reaction_type"] == "LIKE"
    assert react["user"]["id"] == user_data.out.id
    assert react["post_enterprise"]["id"] == post_data.id

@pytest.mark.asyncio
async def test_get_all_by_post_enterprise_id():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    await create_reaction_post_enterprise(
        post_data=post_data,
        reaction=ReactionTypeEnum.DISLIKE,
        user_data=user_data
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?post_enterprise_id={post_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert len(data["items"]) > 0

    react = data["items"][0]
    assert react["user_id"] == user_data.out.id
    assert react["post_enterprise_id"] == post_data.id
    assert react["reaction_type"] == "DISLIKE"
    assert react["user"]["id"] == user_data.out.id
    assert react["post_enterprise"]["id"] == post_data.id

@pytest.mark.asyncio
async def test_return_null_ids_get_all():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = data["body"]

    assert data["message"] == "You must provide either user_id or post_enterprise_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert body is None

@pytest.mark.asyncio
async def test_return_2_ids_get_all():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data.out.id}&post_enterprise_id={post_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = data["body"]

    assert data["message"] == "You must provide either user_id or post_enterprise_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert body is None

@pytest.mark.asyncio
async def test_toggle_create_reaction_like():
    user_data = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data=industry_data)
    category_data = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data=category_data)

    user_data_two = await create_and_login_user()

    dto = CreateReactionPostEnterpriseDTO(
        post_enterprise_id=post_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Reaction added with successfully"
    assert data["code"] == 201
    assert data["status"] is True
    assert data["body"] is None