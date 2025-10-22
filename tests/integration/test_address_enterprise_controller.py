from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_address_user, create_enterprise, create_industry, \
    create_address_to_enterprise
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.address_enterprise_schemas import *
import pytest
from app.configs.db.enums import AddressTypeEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/address-enterprise"

URL_TOGGLE: Final[str] = "/api/v1/address-enterprise/toggle/status/is-public"
URL_EXISTS: Final[str] = "/api/v1/address-enterprise"

@pytest.mark.asyncio
async def test_patch_toggle_status_is_public():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    address_data = await create_address_to_enterprise(user_data, enterprise_data)

    old_status = address_data.is_public

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            URL_TOGGLE,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['code'] == 200
    assert data['message'] == "Address status is public changed with successfully"
    assert data['body']['is_public'] != old_status
    assert data['body']['enterprise_id'] == address_data.enterprise_id

@pytest.mark.asyncio
async def test_patch_toggle_status_is_public_not_found():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            URL_TOGGLE,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['code'] == 404
    assert "not found" in data['message'].lower()

@pytest.mark.asyncio
async def test_exists_by_id_true():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    await create_address_to_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{enterprise_data.id}/exists",
                headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['code'] == 200
    assert data['status'] is True
    assert data['body'] is True

@pytest.mark.asyncio
async def test_exists_by_id_false():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/999999/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['code'] == 200
    assert data['status'] is True
    assert data['body'] is False

@pytest.mark.asyncio
async def test_exists_by_id_bad_request():
    user_data = await create_and_login_user_with_role_super_adm()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL_EXISTS}/0",
                                         headers={"Authorization": f"Bearer {user_data.tokens.token}"})
    data = response.json()
    assert response.status_code == 400
    assert data['code'] == 400
    assert "id is required" in data['message'].lower()

@pytest.mark.asyncio
async def test_patch_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    address_data = await create_address_to_enterprise(user_data, enterprise_data)

    dto = UpdateAddressEnterpriseDTO(
        street="St updated",
        number=None,
        complement=None,
        district=None,
        city=None,
        state=None,
        country=None,
        zipcode=None,
        address_type=None,
        is_default=None,
        is_public=None
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
    assert data['code'] == 200
    assert data['message'] == "Address updated with successfully"
    assert data['body']['enterprise_id'] == address_data.enterprise_id
    assert data['body']['street'] == dto.street
    assert data['body']['number'] == address_data.number

@pytest.mark.asyncio
async def test_return_not_found_patch_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    dto = UpdateAddressEnterpriseDTO(
        street= None,
        number= None,
        complement=None,
        district=None,
        city=None,
        state=None,
        country=None,
        zipcode=None,
        address_type=None,
        is_default=None,
        is_public= None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Address not found"

@pytest.mark.asyncio
async def test_return_not_found_delete_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Address not found"

@pytest.mark.asyncio
async def test_delete_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    address_data = await create_address_to_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is None
    assert data['code'] == 200
    assert data['message'] == "Address deleted with successfully"

@pytest.mark.asyncio
async def test_return_bad_request_get_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400

    assert data['code'] == 400
    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_get_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{999999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['code'] == 404
    assert data['message'] == "Address not found"

@pytest.mark.asyncio
async def test_get_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    address_data = await create_address_to_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{address_data.enterprise_id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body']['enterprise_id'] == address_data.enterprise_id
    assert data['code'] == 200
    assert data['message'] == "Address found with successfully"

@pytest.mark.asyncio
async def test_create_address():
    user_data = await create_and_login_user_with_role_super_adm()

    dto = CreateAddressEnterpriseDTO(
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
        is_public = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['code'] == 404
    assert data['message'] == "Enterprise not found"

@pytest.mark.asyncio
async def test_conflict_exists_address_create_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    address_data = await create_address_to_enterprise(user_data, enterprise_data)

    dto = CreateAddressEnterpriseDTO(
        street="Any ST",
        number="12",
        complement=None,
        district=None,
        city="A",
        state="B",
        country="C",
        zipcode="12345",
        address_type=AddressTypeEnum.RESIDENTIAL,
        is_default=True,
        is_public=True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 403

    assert data['body'] is None
    assert data['code'] == 403
    assert data['message'] == "Address already exists"

@pytest.mark.asyncio
async def test_create_address():
    user_data = await create_and_login_user_with_role_super_adm()
    industry_data = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    dto = CreateAddressEnterpriseDTO(
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
        is_public = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['enterprise_id'] == enterprise_data.id
    assert data['body']['street'] == dto.street
    assert data['body']['number'] == dto.number
    assert data['body']['address_type'] == dto.address_type
    assert data['body']['city'] == dto.city
