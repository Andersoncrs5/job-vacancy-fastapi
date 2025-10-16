from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user, create_category
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

@pytest.mark.asyncio
async def test_return_null_change_status_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"/api/v1/category/{676467564486543}/toggle/status/is_active", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == 404
    assert data["message"] == "Category not found"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_bad_request_change_status_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_negative: Final = await ac.put(f"/api/v1/category/{-45}/toggle/status/is_active", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_negative.status_code == 400

    data = response_negative.json()

    assert data["code"] == 400
    assert data["message"] == "Id is required"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_change_status_category():
    user_data: Final = await create_and_login_user()
    category_data: Final = await create_category(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"/api/v1/category/{category_data.id}/toggle/status/is_active", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == 200
    assert data["message"] == "Category status changed with successfully"
    assert data["status"] == True
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"]["id"] == category_data.id
    assert data["body"]["name"] == category_data.name
    assert data["body"]["description"] == category_data.description
    assert data["body"]["is_active"] == (not category_data.is_active)
    assert data["body"]["order"] == category_data.order
    assert data["body"]["post_count"] == category_data.post_count
    assert data["body"]["job_count"] == category_data.job_count
    assert data["body"]["icon_url"] == category_data.icon_url
    assert data["body"]["user_id"] == category_data.user_id
    assert data["body"]["parent_id"] == category_data.parent_id

@pytest.mark.asyncio
async def test_update_category():
    num = random.randint(10000,100000000000)
    user_data: Final = await create_and_login_user()
    category_data: Final = await create_category(user_data)

    dto = UpdateCategoryDTO(
        name = f"category updated {num}",
        slug = category_data.slug,
        description = "description update",
        order = 8,
        icon_url = None,
        is_active=None,
        parent_id=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put(f"/api/v1/category/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 200

    assert data["code"] == 200
    assert data["message"] == "Category updated with successfully"
    assert data["status"] == True
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"]['id'] == category_data.id
    assert data["body"]['name'] == dto.name
    assert data["body"]['slug'] == category_data.slug
    assert data["body"]['description'] == dto.description
    assert data["body"]['is_active'] == category_data.is_active
    assert data["body"]['order'] == dto.order
    assert data["body"]['post_count'] == category_data.post_count
    assert data["body"]['job_count'] == category_data.job_count
    assert data["body"]['icon_url'] == category_data.icon_url
    assert data["body"]['user_id'] == category_data.user_id
    assert data["body"]['parent_id'] == category_data.parent_id

@pytest.mark.asyncio
async def test_return_bad_request_update_category():
    user_data: Final = await create_and_login_user()

    dto = UpdateCategoryDTO(
        name = None,
        slug = None,
        description = None,
        order = None,
        icon_url = None,
        is_active=None,
        parent_id=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_negative: Final = await ac.put(f"/api/v1/category/{-45}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_negative.status_code == 400

    data = response_negative.json()

    assert data["code"] == 400
    assert data["message"] == "Id is required"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_null_update_category():
    user_data: Final = await create_and_login_user()

    dto = UpdateCategoryDTO(
        name = None,
        slug = None,
        description = None,
        order = None,
        icon_url = None,
        is_active=None,
        parent_id=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.put(f"/api/v1/category/{67646756443}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == 404
    assert data["message"] == "Category not found"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_delete_category():
    user_data: Final = await create_and_login_user()
    category_data: Final = await create_category(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"/api/v1/category/{category_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == 200
    assert data["message"] == "Category deleted with successfully"
    assert data["status"] == True
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_bad_request_delete_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_negative: Final = await ac.delete(f"/api/v1/category/{-45}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_negative.status_code == 400

    data = response_negative.json()

    assert data["code"] == 400
    assert data["message"] == "Id is required"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_null_delete_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"/api/v1/category/{67646756443}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == 404
    assert data["message"] == "Category not found"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_negative: Final = await ac.get(f"/api/v1/category/{-45}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_negative.status_code == 400

    data = response_negative.json()

    assert data["code"] == 400
    assert data["message"] == "Id is required"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_null_get_category():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"/api/v1/category/{67646756443}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == 404
    assert data["message"] == "Category not found"
    assert data["status"] == False
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"] is None

@pytest.mark.asyncio
async def test_get_category():
    user_data: Final = await create_and_login_user()
    category_data: Final = await create_category(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"/api/v1/category/{category_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == 200
    assert data["message"] == "Category found with successfully"
    assert data["status"] == True
    assert data["version"] == 1
    assert data["path"] == None
    assert data["body"]["id"] == category_data.id
    assert data["body"]["name"] == category_data.name
    assert data["body"]["description"] == category_data.description
    assert data["body"]["is_active"] == category_data.is_active
    assert data["body"]["order"] == category_data.order
    assert data["body"]["post_count"] == category_data.post_count
    assert data["body"]["job_count"] == category_data.job_count
    assert data["body"]["icon_url"] == category_data.icon_url
    assert data["body"]["user_id"] == category_data.user_id
    assert data["body"]["parent_id"] == category_data.parent_id

@pytest.mark.asyncio
async def test_create_category():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None,
        parent_id=None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    data = response.json()

    assert data['code'] == 201
    assert data['message'] == 'Category created with successfully'
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None

    assert data['body']['id'] is not None
    assert data['body']['name'] == dto.name
    assert data['body']['slug'] == dto.slug
    assert data['body']['description'] == dto.description
    assert data['body']['order'] == dto.order
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['is_active'] == True
    assert data['body']['user_id'] is not None
    assert data['body']['created_at'] is not None

@pytest.mark.asyncio
async def test_conflict_name_category():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None,
        parent_id=None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_create = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response_create.status_code == 201

    dto.slug += dto.slug + '11'

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_conflict = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response_conflict.status_code == 409

    data = response_conflict.json()

    assert data['code'] == 409
    assert data['message'] == f'Category name: {dto.name} already exists'
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_conflict_slug_category():
    num = random.randint(10000,100000000000)

    user_data = await create_and_login_user()

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None,
        parent_id=None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_create = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response_create.status_code == 201

    dto.name += dto.name + '11'

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_conflict = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response_conflict.status_code == 409

    data = response_conflict.json()

    assert data['code'] == 409
    assert data['message'] == f'Category slug: {dto.slug} already exists'
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None
