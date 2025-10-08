from fastapi.testclient import TestClient
from typing import Final

from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.schemas.industry_schemas import *
from tests.integration.helper import create_and_login_user, create_category, create_post_user, create_comment_post_user
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/comment-post-user"

@pytest.mark.asyncio
async def test_patch_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    dto = UpdateCommentPostUserDTO(
        content = "update" * 50
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.patch(
            f"{URL}/{comment_data.id}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == "Comment updated with successfully"
    assert data['status'] == True

    assert body is not None
    assert body['id'] == comment_data.id
    assert body['content'] == dto.content

@pytest.mark.asyncio
async def test_not_found_patch_comment():
    user_data = await create_and_login_user()

    dto = UpdateCommentPostUserDTO(
        content = "update" * 50
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.patch(
            f"{URL}/{999999999}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 404
    assert data['message'] == "Comment not found"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_bad_request_patch_comment():
    user_data = await create_and_login_user()

    dto = UpdateCommentPostUserDTO(
        content = "update" * 50
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.patch(
            f"{URL}/{0}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_not_found_delete_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{99999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 404
    assert data['message'] == "Comment not found"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_delete_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == "Comment deleted with successfully"
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_get_all_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()

    assert data['items'] is not None

@pytest.mark.asyncio
async def test_bad_request_delete_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_not_found_delete_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{99999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 404
    assert data['message'] == "Comment not found"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_delete_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(
            f"{URL}/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == "Comment deleted with successfully"
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_bad_request_get_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_not_found_get_comment_create_comment():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{99999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 404
    assert data['message'] == "Comment not found"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_get_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 200
    assert data['message'] == "Comment found with successfully"
    assert data['status'] == True

    assert body['id'] == comment_data.id
    assert body['user_id'] == user_data.out.id

@pytest.mark.asyncio
async def test_not_found_post_create_on_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateCommentPostUserDTO(
        content = ("abc" * 50),
        post_user_id = 9999999999,
        parent_comment_id = None
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

    assert data['code'] == 404
    assert data['message'] == 'Post not found'
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_not_found_comment_create_on_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateCommentPostUserDTO(
        content = ("abc" * 50),
        post_user_id = post_user_data.id,
        parent_comment_id = 999999999
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

    assert data['code'] == 404
    assert data['message'] == 'Comment not found'
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_create_on_comment_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    dto = CreateCommentPostUserDTO(
        content = ("abc" * 50),
        post_user_id = post_user_data.id,
        parent_comment_id = comment_data.id
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

    assert data['code'] == 201
    assert data['message'] == 'Comment created with successfully'
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['user_id'] == user_data.out.id
    assert body['post_user_id'] == post_user_data.id

    assert body['user']['id'] == user_data.out.id
    assert body['post']['id'] == post_user_data.id
    assert body['parent_comment_id'] == comment_data.id

@pytest.mark.asyncio
async def test_create_comment():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateCommentPostUserDTO(
        content = ("abc" * 50),
        post_user_id = post_user_data.id,
        parent_comment_id = None
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

    assert data['code'] == 201
    assert data['message'] == 'Comment created with successfully'
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['user_id'] == user_data.out.id
    assert body['post_user_id'] == post_user_data.id

    assert body['user']['id'] == user_data.out.id
    assert body['post']['id'] == post_user_data.id