from fastapi.testclient import TestClient
from typing import Final

from main import app
from httpx import ASGITransport, AsyncClient
import pytest

from tests.integration.helper import (
    create_and_login_user,
    create_category,
    create_post_user,
    create_favorite_comment_user, create_comment_post_user
)

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/favorite-comment-post-user"

@pytest.mark.asyncio
async def test_get_all_no_ids():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            URL,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "You must provide either user_id or comment_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_all_both_ids():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}?user_id={user_data.out.id}&comment_id={comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "You must provide either user_id or comment_id, not both."
    assert data["status"] is False
    assert data["code"] == 400
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_all_user_not_found():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}?user_id=99999999",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "User not found"
    assert data["status"] is False
    assert data["code"] == 404
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_all_comment_not_found():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}?comment_id=99999999",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Comment not found"
    assert data["status"] is False
    assert data["code"] == 404
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_all_success():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)
    await create_favorite_comment_user(user_data, comment_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}?user_id={user_data.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0

    favorite = data["items"][0]
    assert favorite["user_id"] == user_data.out.id
    assert favorite["comment_user_id"] == comment_data.id

@pytest.mark.asyncio
async def test_not_found_favorite_comment_user():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{99999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    assert data['message'] == 'Comment not found'
    assert data['status'] is False
    assert data['code'] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_bad_request_favorite_comment_user():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    assert data['message'] == 'Id is required'
    assert data['status'] is False
    assert data['code'] == 400
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_favorite_comment_user():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)
    await create_favorite_comment_user(user_data, comment_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Comment removed with favorite'
    assert data['status'] is True
    assert data['code'] == 200
    assert data['body'] is None

@pytest.mark.asyncio
async def test_favorite_comment_user():
    user_data = await create_and_login_user()
    category_data = await create_category(user_data)
    post_user_data = await create_post_user(user_data, category_data)
    comment_data = await create_comment_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data['message'] == 'Comment saved with favorite'
    assert data['status'] is True
    assert data['code'] == 201
    assert data['body'] is None
