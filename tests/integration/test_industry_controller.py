from fastapi.testclient import TestClient
from typing import Final
from app.schemas.industry_schemas import *
from tests.integration.helper import create_and_login_user, create_industry
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/industry'

@pytest.mark.asyncio
async def test_update_industry_just_description():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    dto = UpdateIndustryDTO(
        name = None,
        description = "description update",
        icon_url = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{industry_data.id}', json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['message'] == "Industry updated with successfully"
    assert data['status'] == True
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is not None
    assert data['body']['name'] == industry_data.name
    assert data['body']['description'] == dto.description
    assert data['body']['id'] == industry_data.id
    assert data['body']['user_id'] == industry_data.user_id

@pytest.mark.asyncio
async def test_update_industry():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    dto = UpdateIndustryDTO(
        name = f"nome update {random.randint(10000,100000000000)}",
        description = None,
        icon_url = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{industry_data.id}', json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['message'] == "Industry updated with successfully"
    assert data['status'] == True
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is not None
    assert data['body']['name'] == dto.name
    assert data['body']['id'] == industry_data.id
    assert data['body']['user_id'] == industry_data.user_id

@pytest.mark.asyncio
async def test_return_not_found_update_industry():
    user_data: Final = await create_and_login_user()

    dto = UpdateIndustryDTO(
        name = f"nome update {random.randint(10000,100000000000)}",
        description = None,
        icon_url = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{999999999999}', json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Industry not found"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_requet_update_industry():
    user_data: Final = await create_and_login_user()

    dto = UpdateIndustryDTO(
        name = f"nome update {random.randint(10000,100000000000)}",
        description = None,
        icon_url = None,
        is_active = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{-1}', json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.put(f'{URL}/{0}', json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['code'] == 400
    assert data_two['message'] == "Id is required"
    assert data_two['status'] == False
    assert data_two['path'] == None
    assert data_two['version'] == 1
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_exists_industry():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{"ACDC"}/exists', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['message'] == "Industry name not exists"
    assert data['status'] == True
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] == False

@pytest.mark.asyncio
async def test_toggle_status_is_active_industry():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{industry_data.id}/toggle/status/active', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['message'] == "Industry active status changed with successfully"
    assert data['status'] == True
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is not None
    assert data['body']['id'] == industry_data.id
    assert data['body']['user_id'] == industry_data.user_id
    assert data['body']['is_active'] != industry_data.is_active

@pytest.mark.asyncio
async def test_return_not_found_toggle_status_is_active_industry():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{999999999999}/toggle/status/active', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Industry not found"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_requet_toggle_status_is_active_industry():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.put(f'{URL}/{-1}/toggle/status/active', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.get(f'{URL}/{0}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['code'] == 400
    assert data_two['message'] == "Id is required"
    assert data_two['status'] == False
    assert data_two['path'] == None
    assert data_two['version'] == 1
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_industry():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{999999999999}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Industry not found"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_requet_get_industry():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{-1}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.get(f'{URL}/{0}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['code'] == 400
    assert data_two['message'] == "Id is required"
    assert data_two['status'] == False
    assert data_two['path'] == None
    assert data_two['version'] == 1
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_get_industry():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{industry_data.id}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['message'] == "Industry found with successfully"
    assert data['status'] == True
    assert data['path'] == None
    assert data['version'] == 1
    assert data['body']['id'] == industry_data.id
    assert data['body']['user_id'] == industry_data.user_id

@pytest.mark.asyncio
async def test_conflict_name_create_industry():
    num: Final = random.randint(1000,10000000000000)
    user_data: Final = await create_and_login_user()

    dto: Final = CreateIndustryDTO(
        name = f"name {num}",
        description = None,
        icon_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_two.status_code == 409

    data: Final = response_two.json()        

    assert data['message'] == f"Industry name: {dto.name} already exists"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None
    assert data['path'] is None
    assert data['version'] == 1

@pytest.mark.asyncio
async def test_create_industry():
    num: Final = random.randint(1000,10000000000000)
    user_data: Final = await create_and_login_user()

    dto: Final = CreateIndustryDTO(
        name = f"name {num}",
        description = None,
        icon_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    data: Final = response.json()        

    assert data['message'] == "Industry created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert isinstance(data['body']['id'], int)
    assert data['body']['name'] == dto.name
    assert data['body']['description'] == dto.description
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['user_id'] is not None
    assert isinstance(data['body']['user_id'], int)
    assert data['body']['is_active'] == True