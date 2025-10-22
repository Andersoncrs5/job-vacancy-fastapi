from typing import Final

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.configs.db.enums import ReactionTypeEnum
from app.schemas.reaction_comment_post_enterprise_schemas import CreateReactionCommentPostEnterpriseDTO
from main import app
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_category, create_industry, create_enterprise, \
    create_post_enterprise, create_comment_enterprise_user, create_react_comment_post_enterprise

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/area/reaction-comment-enterprise"

@pytest.mark.asyncio
async def test_get_all_filter_by_reaction_type():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()
    user_data_three = await create_and_login_user_with_role_super_adm()

    await create_react_comment_post_enterprise(user_data_two, comment, ReactionTypeEnum.LIKE)
    await create_react_comment_post_enterprise(user_data_three, comment, ReactionTypeEnum.DISLIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?reaction_type={ReactionTypeEnum.LIKE.value}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    react = data['items'][0]
    assert react['reaction_type'] == ReactionTypeEnum.LIKE

@pytest.mark.asyncio
async def test_get_all_by_comment_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()

    await create_react_comment_post_enterprise(user_data_two, comment, ReactionTypeEnum.LIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?comment_enterprise_id={comment.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['items'] is not None
    react = data['items'][0]
    assert react['id'] is not None
    assert react['user_id'] == user_data_two.out.id
    assert react['comment_enterprise_id'] == comment.id
    assert react['reaction_type'] == ReactionTypeEnum.LIKE

@pytest.mark.asyncio
async def test_get_all_by_user_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()

    await create_react_comment_post_enterprise(user_data_two, comment, ReactionTypeEnum.LIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data_two.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['items'] is not None
    react = data['items'][0]
    assert react['id'] is not None
    assert react['user_id'] == user_data_two.out.id
    assert react['comment_enterprise_id'] == comment.id

@pytest.mark.asyncio
async def test_get_all_enterprise_reacts():
    user_data = await create_and_login_user_with_role_super_adm()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            URL,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_change_to_reaction_type_react_comment_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostEnterpriseDTO(
        comment_enterprise_id=comment.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    await create_react_comment_post_enterprise(user_data_two, comment, ReactionTypeEnum.DISLIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['code'] == 200
    assert data['message'] == 'Reaction type changed successfully'
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_react_comment_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostEnterpriseDTO(
        comment_enterprise_id=comment.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    await create_react_comment_post_enterprise(user_data_two, comment, dto.reaction_type)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['code'] == 200
    assert data['message'] == 'Reaction removed with successfully'
    assert data['body'] is None

@pytest.mark.asyncio
async def test_create_react_comment_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category = await create_category(user_data)
    industry = await create_industry(user_data)
    enterprise = await create_enterprise(user_data, industry)
    post_enterprise = await create_post_enterprise(user_data, enterprise, category)
    comment = await create_comment_enterprise_user(user_data, post_enterprise)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostEnterpriseDTO(
        comment_enterprise_id=comment.id,
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
    assert data['code'] == 201
    assert data['body'] is None

@pytest.mark.asyncio
async def test_create_reaction_comment():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise_data: Final = await create_post_enterprise(user_data, enterprise_data, category_data)
    comment_data = await create_comment_enterprise_user(user_data, post_enterprise_data)

    dto = CreateReactionCommentPostEnterpriseDTO(
        comment_enterprise_id=comment_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['code'] == 201

    assert body is None