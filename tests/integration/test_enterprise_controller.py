from fastapi.testclient import TestClient
from typing import Final
from app.schemas.enterprise_schemas import *
from tests.integration.helper import create_and_login_user, create_industry, create_enterprise
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/enterprise'






@pytest.mark.asyncio
async def test_exists_by_name_enterprise():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{"aaaa"}/exists/name', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Enterprise name not exists"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] == False

@pytest.mark.asyncio
async def test_delete_enterprise():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.delete(f'{URL}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Enterprise deleted with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_not_found_delete_enterprise():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{222283423214545}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Enterprise not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_bad_request_get_enterprise():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{-22223423214545}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.get(f'{URL}/{0}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    assert response_two.status_code == 400

    assert data_two['message'] == "Id is required"
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['version'] == 1
    assert data_two['path'] == None
    assert data_two['body'] is None

@pytest.mark.asyncio
async def test_not_found_get_enterprise():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{22223423214545}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Enterprise not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_enterprise():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/{enterprise_data.id}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Enterprise found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body']['id'] == enterprise_data.id
    assert data['body']['name'] == enterprise_data.name
    assert data['body']['description'] == enterprise_data.description

@pytest.mark.asyncio
async def test_not_found_get_my_enterprise():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/my', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Enterprise not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_my_enterprise():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}/my', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Enterprise found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] == None
    assert data['body']['id'] == enterprise_data.id
    assert data['body']['name'] == enterprise_data.name
    assert data['body']['description'] == enterprise_data.description

@pytest.mark.asyncio
async def test_create_enterprise():
    num: Final = random.randint(1000,10000000000000)

    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data: Final = response.json()

    assert response.status_code == 201

    assert data['message'] == 'Enterprise created with successfully'
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['user_id'] is not None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_return_not_found_industry_create_enterprise():
    num: Final = random.randint(1000,10000000000000)

    user_data: Final = await create_and_login_user()

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{8888888989}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data: Final = response.json()

    assert response.status_code == 404

    assert data['message'] == 'Industry not found'
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_return_bad_request_industry_create_enterprise():
    num: Final = random.randint(1000,10000000000000)

    user_data: Final = await create_and_login_user()

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{-99}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data: Final = response.json()

    assert response.status_code == 400

    assert data['message'] == 'Id is required'
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two = await acdc.post(F"{URL}/{0}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two: Final = response_two.json()

    assert response_two.status_code == 400

    assert data_two['message'] == 'Id is required'
    assert data_two['code'] == 400
    assert data_two['status'] == False
    assert data_two['body'] is None
    assert data_two['version'] == 1
    assert data_two['path'] is None

@pytest.mark.asyncio
async def test_confict_name_create_enterprise():
    num: Final = random.randint(1000,10000000000000)

    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_confict = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_confict.status_code == 409

    data = response_confict.json()

    assert data['message'] == f"Name {dto.name} are in use"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None

@pytest.mark.asyncio
async def test_confict_user_create_enterprise():
    num: Final = random.randint(1000,10000000000000)

    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    dto.name += f"{num}"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_confict = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response_confict.status_code == 409

    data = response_confict.json()

    assert data['message'] == f"You already have a enterprise"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None
    assert data['version'] == 1
    assert data['path'] is None