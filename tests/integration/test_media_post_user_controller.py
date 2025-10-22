from fastapi.testclient import TestClient
from typing import Final
from app.schemas.media_post_user_schemas import *
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_media_post_user, create_post_user, create_category, create_favorite_post_user
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/media-post-user'

@pytest.mark.asyncio
async def test_return_bad_request_patch_media():
    user_data = await create_and_login_user_with_role_super_adm()

    dto: Final = UpdateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = None,
        order = None,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{0}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_patch_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)

    dto: Final = UpdateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = None,
        order = None,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{999999999999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['message'] == "Media not found"
    assert data['code'] == 404
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_patch_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    media_post_user_data = await create_media_post_user(user_data, post_user_data)

    dto: Final = UpdateMediaPostUserDTO(
        url = "https://picsum.photos/500/800",
        type = None,
        order = 8,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{media_post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is not None
    assert data['body']['id'] == media_post_user_data.id 
    assert data['body']['url'] == dto.url
    assert data['body']['order'] == dto.order
    assert data['message'] == "Media updated with successfully"
    assert data['code'] == 200
    assert data['version'] == 1
    assert data['status'] == True

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert isinstance(data['total'], int)
    assert isinstance(data['page'], int)
    assert isinstance(data['size'], int)
    assert isinstance(data['pages'], int)

@pytest.mark.asyncio
async def test_return_bad_request_get_media():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_get_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    media_post_user_data = await create_media_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{88899999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['message'] == "Media not found"
    assert data['code'] == 404
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_get_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    media_post_user_data = await create_media_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{media_post_user_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is not None
    assert data['path'] is None
    assert data['message'] == "Media found with successfully"
    assert data['code'] == 200
    assert data['version'] == 1
    assert data['status'] == True

@pytest.mark.asyncio
async def test_return_bad_request_delete_media():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_delete_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    media_post_user_data = await create_media_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{88899999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['message'] == "Media not found"
    assert data['code'] == 404
    assert data['version'] == 1
    assert data['status'] == False

@pytest.mark.asyncio
async def test_delete_media():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)
    media_post_user_data = await create_media_post_user(user_data, post_user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{media_post_user_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is None
    assert data['message'] == "Media deleted with successfully"
    assert data['code'] == 200
    assert data['version'] == 1
    assert data['status'] == True

@pytest.mark.asyncio
async def test_return_not_found_create_media_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)

    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}/{999999999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Post user not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body']is None

@pytest.mark.asyncio
async def test_return_bad_request_create_media_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}/{0}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Post user id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body']is None

@pytest.mark.asyncio
async def test_create_media_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Media created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['post_id'] == post_user_data.id

@pytest.mark.asyncio
async def test_return_conflict_create_media_post_user():
    user_data = await create_and_login_user_with_role_super_adm()
    category_data: Final = await create_category(user_data)
    post_user_data: Final = await create_post_user(user_data, category_data)

    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        for i in range(10):
            await acdc.post(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    
    assert response.status_code == 409

    assert data['message'] == "Limit to midia by post are 10"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None