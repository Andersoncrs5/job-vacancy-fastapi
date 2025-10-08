from typing import Final

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.configs.db.enums import ReactionTypeEnum
from app.schemas.reaction_post_user_schemas import CreateReactionPostUserDTO
from main import app
from tests.integration.helper import create_post_user, create_and_login_user, create_category, create_reaction_post_user

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/area/reaction-post-user"
URL_TOGGLE = "/api/v1/area/reaction-post-user/toggle"


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

    assert data["message"] == "You must provide either user_id or post_user_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert body is None

@pytest.mark.asyncio
async def test_return_2_ids_get_all():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data.out.id}&post_user_id={post_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = data["body"]

    assert data["message"] == "You must provide either user_id or post_user_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert body is None

@pytest.mark.asyncio
async def test_get_all_by_user_id():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)

    await create_reaction_post_user(
        post_user_data=post_data,
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
    assert react["post_user_id"] == post_data.id
    assert react["reaction_type"] == "LIKE"
    assert react["user"]["id"] == user_data.out.id
    assert react["post"]["id"] == post_data.id

@pytest.mark.asyncio
async def test_get_all_by_post_user_id():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)

    await create_reaction_post_user(
        post_user_data=post_data,
        reaction=ReactionTypeEnum.DISLIKE,
        user_data=user_data
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?post_user_id={post_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert len(data["items"]) > 0

    react = data["items"][0]
    assert react["user_id"] == user_data.out.id
    assert react["post_user_id"] == post_data.id
    assert react["reaction_type"] == "DISLIKE"
    assert react["user"]["id"] == user_data.out.id
    assert react["post"]["id"] == post_data.id

@pytest.mark.asyncio
async def test_toggle_create_reaction_like():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)

    dto = CreateReactionPostUserDTO(
        post_user_id=post_user_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL_TOGGLE,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Reaction added with successfully"
    assert data["code"] == 201
    assert data["status"] is True
    assert data["body"] is None

@pytest.mark.asyncio
async def test_toggle_remove_reaction_like():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)

    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    dto = CreateReactionPostUserDTO(
        post_user_id=post_user_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL_TOGGLE,
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
async def test_toggle_change_reaction_like_to_dislike():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)

    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    dto = CreateReactionPostUserDTO(
        post_user_id=post_user_data.id,
        reaction_type=ReactionTypeEnum.DISLIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL_TOGGLE,
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
async def test_toggle_post_not_found():
    user_data = await create_and_login_user()

    dto = CreateReactionPostUserDTO(
        post_user_id=999999,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL_TOGGLE,
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
async def test_bad_request_get_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{9999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction not found"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_bad_request_get_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_get_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{post_user_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction found with successfully"
    assert data['code'] == 200

    assert body is not None
    assert body['user_id'] == user_data.out.id
    assert body['post_user_id'] == post_user_data.id

@pytest.mark.asyncio
async def test_bad_request_delete_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{9999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction not found"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_bad_request_delete_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_delete_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{post_user_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction deleted with successfully"
    assert data['code'] == 200

    assert body is None

@pytest.mark.asyncio
async def test_not_found_post_create_reaction_like_to_post():
    user_data = await create_and_login_user()

    dto = CreateReactionPostUserDTO(
        post_user_id = 9999999,
        reaction_type = ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Post not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_conflict_create_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    await create_reaction_post_user(post_user_data=post_user_data, reaction=ReactionTypeEnum.LIKE, user_data=user_data)

    dto = CreateReactionPostUserDTO(
        post_user_id=post_user_data.id,
        reaction_type=ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 409
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "You have already reacted to this post"
    assert data['code'] == 409

    assert body is None

@pytest.mark.asyncio
async def test_create_reaction_like_to_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateReactionPostUserDTO(
        post_user_id = post_user_data.id,
        reaction_type = ReactionTypeEnum.LIKE
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction added with successfully"
    assert data['code'] == 201

    assert body is None
