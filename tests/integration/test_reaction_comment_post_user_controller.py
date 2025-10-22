from typing import Final

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.configs.db.enums import ReactionTypeEnum
from app.schemas.reaction_comment_post_user_schemas import CreateReactionCommentPostUserDTO
from app.schemas.reaction_post_enterprise_schemas import CreateReactionPostEnterpriseDTO
from main import app
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_category, create_post_enterprise, create_enterprise, \
    create_industry, create_reaction_post_enterprise, create_post_user, create_comment_post_user, \
    create_react_comment_post_user

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/area/reaction-comment-user"

@pytest.mark.asyncio
async def test_get_all_by_comment():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    user_data_two = await create_and_login_user_with_role_super_adm()

    await create_react_comment_post_user(user_data_two, comment_data, ReactionTypeEnum.LIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?comment_user_id={comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()

    assert data['items'] is not None

    react = data['items'][0]

    assert react['id'] is not None
    assert react['user_id'] == user_data_two.out.id
    assert react['comment_user_id'] == comment_data.id
    assert react['reaction_type'] == ReactionTypeEnum.LIKE

@pytest.mark.asyncio
async def test_get_all_by_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    user_data_two = await create_and_login_user_with_role_super_adm()

    await create_react_comment_post_user(user_data_two, comment_data, ReactionTypeEnum.LIKE)

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
    assert react['comment_user_id'] == comment_data.id

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            URL,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_change_to_reaction_type_react_comment_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostUserDTO(
        comment_user_id=comment_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    await create_react_comment_post_user(user_data_two, comment_data, ReactionTypeEnum.DISLIKE)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == 'Reaction type changed successfully'

    assert body is None

@pytest.mark.asyncio
async def test_delete_react_comment_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostUserDTO(
        comment_user_id=comment_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    await create_react_comment_post_user(user_data_two, comment_data, dto.reaction_type)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == 'Reaction removed with successfully'

    assert body is None

@pytest.mark.asyncio
async def test_create_react_comment_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    user_data_two = await create_and_login_user_with_role_super_adm()

    dto = CreateReactionCommentPostUserDTO(
        comment_user_id=comment_data.id,
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
    body = response.json()['body']

    assert data['code'] == 201

    assert body is None