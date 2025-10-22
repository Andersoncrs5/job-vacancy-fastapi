from fastapi.testclient import TestClient
from typing import Final
from app.schemas.enterprise_schemas import *
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_enterprise, create_post_user, create_category, create_favorite_post_user
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/favorite-post-user'


@pytest.mark.asyncio
async def test_return_bad_request_check_exists():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data: Final[int] = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f"{URL}/{-9}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.get(f"{URL}/{0}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()

    assert response_two.status_code == 400

    assert data_two['message'] == "Id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['body'] is None
    assert data_two['path'] is None
    assert data_two['version'] == 1

@pytest.mark.asyncio
async def test_check_exists():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data: Final[int] = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f"{URL}/{post_data.id}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 200

    assert data['message'] == "Favorite post name already exists"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] == True
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_return_not_found_delete_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data: Final[int] = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.delete(f"{URL}/{99999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 404

    assert data['message'] =="Post not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_return_bad_request_delete_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data: Final[int] = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.delete(f"{URL}/{-9}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 400

    assert data['message'] =="Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()

    assert response_two.status_code == 400

    assert data_two['message'] =="Id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['body'] is None
    assert data_two['path'] is None
    assert data_two['version'] == 1

@pytest.mark.asyncio
async def test_delete_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data: Final[int] = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.delete(f"{URL}/{favorite_data}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 200

    assert data['message'] =="Post removed with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_return_conflict_post_create_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    favorite_data = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{post_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 409

    assert data['message'] =="Post are already saved how favorite"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_return_not_found_post_create_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{9999999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 404

    assert data['message'] =="Post user not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_bad_request_create_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)
    # favorite_data = await create_favorite_post_user(user_data, category_data, post_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{-9}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 400

    assert data['message'] =="Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.post(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()

    assert response_two.status_code == 400

    assert data_two['message'] =="Id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['body'] is None
    assert data_two['path'] is None
    assert data_two['version'] == 1

@pytest.mark.asyncio
async def test_create_favorite_post():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    post_data = await create_post_user(user_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{post_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 201

    assert data['message'] =="Post favorited with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body'] is not None
    assert data['path'] is None
    assert data['version'] == 1