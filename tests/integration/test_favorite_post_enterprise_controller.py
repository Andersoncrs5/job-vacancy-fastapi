from fastapi.testclient import TestClient
from typing import Final
from app.schemas.enterprise_schemas import *
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_industry, create_favorite_post_enterprise, create_category, create_enterprise, create_post_enterprise
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/favorite-post-enterprise'


@pytest.mark.asyncio
async def test_exists_favorite_return_bad_request():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/0/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data["message"] == "Id is required"
    assert data["code"] == 400
    assert data["status"] is False
    assert data["body"] is None

@pytest.mark.asyncio
async def test_exists_favorite_when_not_exists():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{post_enterprise.id}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Favorite post not exists"
    assert data["code"] == 200
    assert data["status"] is True
    assert data["body"] is False

@pytest.mark.asyncio
async def test_exists_favorite_when_exists():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise = await create_post_enterprise(user_data, enterprise_data, category_data)
    await create_favorite_post_enterprise(user_data, post_enterprise)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}/{post_enterprise.id}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Favorite post already exists"
    assert data["code"] == 200
    assert data["status"] is True
    assert data["body"] is True

@pytest.mark.asyncio
async def test_return_not_found_get_all_by_user_id():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{99999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "User not found"
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_all_by_user_id():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_all_by_user_id():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{user_data.out.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_delete_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise = await create_post_enterprise(user_data, enterprise_data, category_data)
    favorite_id = await create_favorite_post_enterprise(user_data, post_enterprise)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{favorite_id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post removed with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_not_found_post_delete_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{9999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post not found"
    assert data['code'] == 404
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_bad_request_post_delete_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_bad_request_post_create_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_post_create_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{9999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post not found"
    assert data['code'] == 404
    assert data['status'] == False

@pytest.mark.asyncio
async def test_conflict_exists_create_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise = await create_post_enterprise(user_data, enterprise_data, category_data)
    await create_favorite_post_enterprise(user_data, post_enterprise)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{post_enterprise.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 409

    assert data['message'] == "Post are already saved how favorite"
    assert data['code'] == 409
    assert data['status'] == False

@pytest.mark.asyncio
async def test_create_favorite_post_enterprise():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data = await create_category(user_data)
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    post_enterprise = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{post_enterprise.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Post favorited with successfully"
    assert data['code'] == 201
    assert data['status'] == True