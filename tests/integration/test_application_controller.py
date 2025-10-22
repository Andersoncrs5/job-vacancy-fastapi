from typing import Final

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.configs.db.enums import ApplicationStatusEnum
from app.schemas.application_schemas import UpdateApplicationDTO
from main import app
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_industry, create_enterprise, create_area, \
    create_vacancy, UserTestData, create_application

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/application"

@pytest.mark.asyncio
async def test_patch_return_not_found_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()

    dto = UpdateApplicationDTO(
        status=None,
        is_viewed=None,
        priority_level=None,
        rating=None,
        feedback=None,
        source=None,
        notes=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{9999999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"},
            json=dict(dto)
        )

    assert response.status_code == 404
    data = response.json()

    assert data["message"] == "Application not found"
    assert data["code"] == 404
    assert data["status"] is False

@pytest.mark.asyncio
async def test_patch_application_successfully():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    application = await create_application(user_data, vacancy_data)

    dto = UpdateApplicationDTO(
        status = ApplicationStatusEnum.REJECTED,
        is_viewed=None,
        priority_level=None,
        rating=1,
        feedback=None,
        source=None,
        notes=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{application.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"},
            json=dict(dto),
        )

    assert response.status_code == 200
    data = response.json()
    body = data["body"]

    assert data["message"] == "Application updated with successfully"
    assert data["code"] == 200
    assert data["status"] is True
    assert isinstance(body, dict)
    assert body["id"] == application.id
    assert body["vacancy_id"] == vacancy_data.id
    assert body["user_id"] == user_data.out.id

    assert body['status'] == dto.status
    assert body['source'] == application.source
    assert body['rating'] == dto.rating

@pytest.mark.asyncio
async def test_patch_return_bad_request_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()

    dto = UpdateApplicationDTO(
        status=None,
        is_viewed=None,
        priority_level=None,
        rating=None,
        feedback=None,
        source=None,
        notes=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"},
        )

    assert response.status_code == 400
    data = response.json()

    assert data["message"] == "Id is required"
    assert data["code"] == 400
    assert data["status"] is False

@pytest.mark.asyncio
async def test_delete_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    user_data_two: UserTestData = await create_and_login_user_with_role_super_adm()

    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    application = await create_application(user_data_two, vacancy_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{application.id}",
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 403

    data = response.json()

    assert data['message'] == 'You are not authorized to removed this application'
    assert data['code'] == 403
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_vacancy_delete_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400

    data = response.json()

    assert data['message'] == 'Id is required'
    assert data['code'] == 400
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_vacancy_delete_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{9999999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()

    assert data['message'] == 'Application not found'
    assert data['code'] == 404
    assert data['status'] == False

@pytest.mark.asyncio
async def test_delete_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    application = await create_application(user_data, vacancy_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{application.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()

    assert data['message'] == 'Application removed with successfully'
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_all():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()

    assert data['items'] is not None
    assert data['total'] is not None and isinstance(data['total'], int) == True
    assert data['page'] is not None and isinstance(data['page'], int) == True
    assert data['size'] is not None and isinstance(data['size'], int) == True
    assert data['pages'] is not None and isinstance(data['pages'], int) == True

@pytest.mark.asyncio
async def test_conflict_exists_create_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    application = await create_application(user_data, vacancy_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{vacancy_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 409

    data = response.json()
    body = response.json()['body']

    assert data['message'] == 'You have already applied for this position!'
    assert data['code'] == 409
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_vacancy_create_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{9999999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()

    assert data['message'] == 'Vacancy not found'
    assert data['code'] == 404
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_bad_request_vacancy_create_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400

    data = response.json()

    assert data['message'] == 'Id is required'
    assert data['code'] == 400
    assert data['status'] == False

@pytest.mark.asyncio
async def test_create_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{vacancy_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

    data = response.json()
    body = response.json()['body']

    assert data['message'] == 'Application sent successfully'
    assert data['code'] == 201
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['vacancy_id'] == vacancy_data.id
    assert body['user_id'] == user_data.out.id
