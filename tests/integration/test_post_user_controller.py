from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user, create_category, create_post_user
from main import app
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

URL: Final[str] = "/api/v1/post-user"

@pytest.mark.asyncio
async def test_return_not_found_put_post_by_id():
    user_data = await create_and_login_user()

    dto = UpdatePostUserDTO(
        title = None,
        content = None,
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"{URL}/{99999999999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post user not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_put_post_by_id():
    user_data = await create_and_login_user()

    dto = UpdatePostUserDTO(
        title = None,
        content = None,
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"{URL}/{-1}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_two: Final = await ac.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['message'] == "Post user id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['version'] == 1
    assert data_two['path'] is None
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_update_post():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = UpdatePostUserDTO(
        title = "title update 1111111111",
        content = "Content update",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post updated with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body']['id'] == post_user_data.id
    assert data['body']['title'] == dto.title
    assert data['body']['content'] == dto.content
    assert data['body']['user_id'] == post_user_data.user_id
    assert data['body']['category_id'] == category_data.id

@pytest.mark.asyncio
async def test_return_not_found_delete_post_by_id():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{99999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post user not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_delete_post_by_id():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{-1}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_two: Final = await ac.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['message'] == "Post user id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['version'] == 1
    assert data_two['path'] is None
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_delete_post_user():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{post_user_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post deleted with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_category_create_post_user():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreatePostUserDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{9999999999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Category not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_return_bad_request_create_post_user():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreatePostUserDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{-9999999999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_post_by_id():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{99999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post user not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_post_by_id():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{-1}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_two: Final = await ac.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['message'] == "Post user id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['version'] == 1
    assert data_two['path'] is None
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_get_post_user():
    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{post_user_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body']['id'] == post_user_data.id
    assert data['body']['user_id'] == post_user_data.user_id

@pytest.mark.asyncio
async def test_create_post_user():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()
    category_data: Final = await create_category(user_data)

    dto = CreatePostUserDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Post created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['title'] == dto.title
    assert data['body']['content'] == dto.content
    assert data['body']['url_image'] == dto.url_image
    assert data['body']['category_id'] == category_data.id
