from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, create_address_user
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.address_user_schemas import *
import pytest
import random
from app.configs.db.enums import AddressTypeEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/address-user"

@pytest.mark.asyncio
async def test_bad_request_found_exists_address():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}/exists", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_exists_by_user_id_address():
    user_data = await create_and_login_user()
    address_data = await create_address_user(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{address_data.user_id}/exists", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['body'] == True

@pytest.mark.asyncio
async def test_patch_address():
    user_data = await create_and_login_user()
    address_data = await create_address_user(user_data)

    dto = UpdateAddressUserDTO(
        street = "Any ST updated",
        number = None,
        complement = None,
        district = None,
        city = None,
        state = None,
        country = "US",
        zipcode = None,
        address_type = None,
        is_default = None,
        is_visible=True,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is not None
    assert data['body']['id'] == address_data.id
    assert data['body']['user_id'] == address_data.user_id
    assert data['body']['street'] == dto.street
    assert data['body']['number'] == address_data.number
    assert data['body']['complement'] == address_data.complement
    assert data['body']['country'] == dto.country

@pytest.mark.asyncio
async def test_return_not_found_patch_address():
    user_data = await create_and_login_user()

    dto = UpdateAddressUserDTO(
        street = "Any ST updated",
        number = None,
        complement = None,
        district = None,
        city = None,
        state = None,
        country = None,
        zipcode = None,
        address_type = None,
        is_default = None,
        is_visible=True,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_delete_address():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['message'] == "Address not found"

@pytest.mark.asyncio
async def test_delete_address():
    user_data = await create_and_login_user()
    address_data = await create_address_user(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['body'] is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two: Final = await acdc.get(
            f"{URL}/{address_data.user_id}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response_two.status_code == 404

@pytest.mark.asyncio
async def test_bad_request_found_get_address():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_get_address():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{9999999}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['message'] == "Address not found"

@pytest.mark.asyncio
async def test_get_address():
    user_data = await create_and_login_user()
    address_data = await create_address_user(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{address_data.user_id}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['body']['id'] == address_data.id
    assert data['body']['street'] == address_data.street
    assert data['body']['user_id'] == address_data.user_id

@pytest.mark.asyncio
async def test_conflict_exists_address_create_address():
    user_data = await create_and_login_user()
    address_data = await create_address_user(user_data)

    dto = CreateAddressUserDTO(
        street = "Any ST",
        number = "12",
        complement = None,
        district = None,
        city = "A",
        state = "B",
        country = "C",
        zipcode = "12345",
        address_type = AddressTypeEnum.RESIDENTIAL,
        is_default = True,
        is_visible = True,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 409

    assert data['code'] == 409
    assert data['message'] == "You already have a address"
    assert data['body'] is None
    
@pytest.mark.asyncio
async def test_create_address():
    user_data = await create_and_login_user()

    dto = CreateAddressUserDTO(
        street = "Any ST",
        number = "12",
        complement = None,
        district = None,
        city = "A",
        state = "B",
        country = "C",
        zipcode = "12345",
        address_type = AddressTypeEnum.RESIDENTIAL,
        is_default = True,
        is_visible=True,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['user_id'] == user_data.out.id
    assert data['body']['street'] == dto.street