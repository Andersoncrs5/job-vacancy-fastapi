from fastapi.testclient import TestClient
from typing import Final
from app.schemas.category_schemas import *
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_category, create_enterprise, create_industry, create_post_enterprise
from main import app
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)

URL: Final[str] = "/api/v1/post-enterprise"

@pytest.mark.asyncio
async def test_get_metric_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{post_data.id}/metric", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post metric found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body']['post_id'] == post_data.id

@pytest.mark.asyncio 
async def test_update_post_success(): 
    user_data = await create_and_login_user_with_role_super_adm()
    industry = await create_industry(user_data) 
    enterprise = await create_enterprise(user_data, industry) 
    category = await create_category(user_data) 
    post = await create_post_enterprise(user_data, enterprise, category) 
    new_title = f"Updated title {random.randint(1,10000)}" 
    new_content = "This is an updated content" 

    dto = UpdatePostEnterpriseDTO(title=new_title, content=new_content, url_image="http://newimage.com/img.png") 

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac: 
        response = await ac.put(f"{URL}/{post.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"}) 
    
    data = response.json() 
    assert response.status_code == 200 
    assert data["message"] == "Post updated with successfully" 
    assert data["code"] == 200 
    assert data["status"] is True 
    assert data["body"]["id"] == post.id 
    assert data["body"]["title"] == new_title 
    assert data["body"]["content"] == new_content 
    assert data["body"]["url_image"] == dto.url_image

@pytest.mark.asyncio 
async def test_update_post_not_found(): 
    user_data = await create_and_login_user_with_role_super_adm()
    dto = UpdatePostEnterpriseDTO(title="Does not exist", content="Not found", url_image=None) 

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac: 
        response = await ac.put(f"{URL}/999999999", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"}) 

    data = response.json() 
    assert response.status_code == 404 
    assert data["message"] == "Post not found"
    assert data["code"] == 404 
    assert data["status"] is False 
    assert data["body"] is None

@pytest.mark.asyncio 
async def test_update_post_bad_request_id_zero(): 
    user_data = await create_and_login_user_with_role_super_adm()
    dto = UpdatePostEnterpriseDTO(title="New title", content="Updated content", url_image=None) 

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac: 
        response = await ac.put(f"{URL}/0", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"}) 
    data = response.json() 
    assert response.status_code == 400 
    assert data["message"] == "Post user id is required" 
    assert data["code"] == 400 
    assert data["status"] is False 
    assert data["body"] is None

@pytest.mark.asyncio
async def test_return_not_found_delete_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_delete_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.delete(f"{URL}/{post_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post deleted with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)
    post_data = await create_post_enterprise(user_data, enterprise_data, category_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}/{post_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Post found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None
    assert data['body']['id'] == post_data.id
    assert data['body']['enterprise_id'] == post_data.enterprise_id
    assert data['body']['title'] == post_data.title
    assert data['body']['content'] == post_data.content

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_return_not_found_enterprise_create_post_enterprise():
    num = random.randint(10000,10000000000000)

    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    category_data: Final = await create_category(user_data)

    dto = CreatePostEnterpriseDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Enterprise not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_create_post_enterprise():
    num = random.randint(10000,10000000000000)

    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)

    dto = CreatePostEnterpriseDTO(
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

@pytest.mark.asyncio
async def test_return_bad_request_create_post_enterprise():
    num = random.randint(10000,10000000000000)

    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)

    dto = CreatePostEnterpriseDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{0}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_create_post_enterprise():
    num = random.randint(10000,10000000000000)

    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    category_data: Final = await create_category(user_data)

    dto = CreatePostEnterpriseDTO(
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
    assert data['body']['enterprise_id'] == enterprise_data.id