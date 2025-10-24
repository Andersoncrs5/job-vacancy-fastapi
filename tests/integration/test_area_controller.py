from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_area, create_and_login_user_with_role_super_adm, \
    create_and_login_user_without_role
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.area_schemas import *
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/area'

@pytest.mark.asyncio
async def test_return_bad_request_update_area():
    user_data = await create_and_login_user_with_role_super_adm()

    dto = UpdateAreaDTO(
        name = None,
        description = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data['body'] is None
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_update_area():
    user_data = await create_and_login_user_with_role_super_adm()

    dto = UpdateAreaDTO(
        name = None,
        description = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{999999999}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['body'] is None
    assert data['message'] == "Area not found"

@pytest.mark.asyncio
async def test_update_area():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)
    num = random.randint(10000,100000000000000)

    dto = UpdateAreaDTO(
        name = f"name updated {num}",
        description = "any description",
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{area_data.id}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['body'] is not None
    assert data['message'] == "Area updated with successfully"
    assert data['body']['id'] == area_data.id
    assert data['body']['user_id'] == area_data.user_id
    assert data['body']['is_active'] == area_data.is_active
    assert data['body']['name'] == dto.name
    assert data['body']['description'] == dto.description

@pytest.mark.asyncio
async def test_return_not_authorized_update_area():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_without_roles = await create_and_login_user_without_role()

    area_data = await create_area(user_data)
    num = random.randint(10000,100000000000000)

    dto = UpdateAreaDTO(
        name = f"name updated {num}",
        description = "any description",
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{area_data.id}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_without_roles.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 401
    assert data['body'] is None
    assert data['code'] == 401
    assert data['message'] == "You are not authorized"

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_filter_by_name_get_all():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}?name__ilike={area_data.name}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['items'][0]['name'] == area_data.name

@pytest.mark.asyncio
async def test_filter_by_is_active_and_name_get_all():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}?name__ilike={area_data.name}&is_active={area_data.is_active}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['items'][0]['name'] == area_data.name

@pytest.mark.asyncio
async def test_return_bad_request_toggle_active_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}/toggle/status/is-active", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data['body'] is None
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_toggle_active_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{999999999}/toggle/status/is-active", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['body'] is None
    assert data['message'] == "Area not found"

@pytest.mark.asyncio
async def test_toggle_active_area():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{area_data.id}/toggle/status/is-active", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['body'] is not None
    assert data['message'] == "Area status is active changed with successfully"
    assert data['body']['id'] == area_data.id
    assert data['body']['user_id'] == area_data.user_id
    assert data['body']['is_active'] == (not area_data.is_active)

@pytest.mark.asyncio
async def test_return_not_authorized_active_area():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_no_roles = await create_and_login_user_without_role()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{area_data.id}/toggle/status/is-active",
            headers={"Authorization": f"Bearer {user_data_no_roles.tokens.token}"}
        )

    data = response.json()

    assert response.status_code == 401
    assert data['body'] is None
    assert data['code'] == 401
    assert data['message'] == "You are not authorized"

@pytest.mark.asyncio
async def test_return_bad_request_delete_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400
    assert data['body'] is None
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_delete_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{99999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404
    assert data['body'] is None
    assert data['message'] == "Area not found"

@pytest.mark.asyncio
async def test_delete_area():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{area_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200
    assert data['body'] is None
    assert data['message'] == "Area deleted with successfully"

@pytest.mark.asyncio
async def test_return_not_authorized__area():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_no_roles = await create_and_login_user_without_role()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{area_data.id}", headers={"Authorization": f"Bearer {user_data_no_roles.tokens.token}"})

    data = response.json()
    assert response.status_code == 401
    assert data['body'] is None
    assert data['code'] == 401
    assert data['message'] == "You are not authorized"

@pytest.mark.asyncio
async def test_bad_request_found_get_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_get_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{9999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404
    assert data['message'] == "Area not found"

@pytest.mark.asyncio
async def test_get_area():
    user_data = await create_and_login_user_with_role_super_adm()
    area_data = await create_area(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{area_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200
    assert data['body']['id'] == area_data.id
    assert data['body']['name'] == area_data.name
    assert data['body']['user_id'] == area_data.user_id

@pytest.mark.asyncio
async def test_conflict_with_name_create_area():
    num = random.randint(10000,100000000000000)
    user_data = await create_and_login_user_with_role_super_adm()

    dto = CreateAreaDTO(
        name = f"name {num}",
        description = None,
        is_active = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 409

    assert data_two['body'] is None
    assert data_two['message'] == f"Name {dto.name} is in use! Try another name"
    assert data_two['code'] == 409

@pytest.mark.asyncio
async def test_create_area():
    num = random.randint(10000,100000000000000)
    user_data = await create_and_login_user_with_role_super_adm()

    dto = CreateAreaDTO(
        name = f"name {num}",
        description = None,
        is_active = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['name'] == dto.name
    assert data['body']['is_active'] == dto.is_active
    assert data['body']['user_id'] == user_data.out.id

@pytest.mark.asyncio
async def test_return_401_create_area():
    num = random.randint(10000,100000000000000)
    user_data = await create_and_login_user_without_role()

    dto = CreateAreaDTO(
        name = f"name {num}",
        description = None,
        is_active = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_exists_name_area():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{"any name"}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['body'] == False