from fastapi.testclient import TestClient
from typing import Final
from app.schemas.review_enterprise_schemas import *
from tests.integration.helper import (
    create_and_login_user_with_role_super_adm, create_industry,
    create_enterprise, create_employee, create_review
)
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from datetime import date
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/review-enterprise'

@pytest.mark.asyncio
async def test_return_bad_request_update_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()

    dto = UpdateReviewEnterpriseDTO(
        title="new title",
        description=("new description" * 20 ),
        rating = None,
        pros = None,
        cons = None,
        would_recommend = None,
        position = None,
        salary_range = None,
        employment_type = None,
        employment_status = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{0}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400
    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_update_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()

    dto = UpdateReviewEnterpriseDTO(
        title="new title",
        description=("new description" * 20 ),
        rating = None,
        pros = None,
        cons = None,
        would_recommend = None,
        position = None,
        salary_range = None,
        employment_type = None,
        employment_status = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{999999}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404
    assert data['message'] == "Review not found"
    assert data['code'] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_update_review_within_7_days():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    user_data_two: Final = await create_and_login_user_with_role_super_adm()
    employee_data = await create_employee(user_data, enterprise_data, user_data_two)
    review_data = await create_review(user_data, enterprise_data, user_data_two)

    dto = UpdateReviewEnterpriseDTO(
        title="new title",
        description=("new description" * 20 ),
        rating = None,
        pros = None,
        cons = None,
        would_recommend = None,
        position = None,
        salary_range = None,
        employment_type = None,
        employment_status = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{review_data.id}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Review updated with successfully"
    assert data['code'] == 200
    assert data['status'] is True
    assert data['body']['title'] == dto.title
    assert data['body']['description'] == dto.description

@pytest.mark.asyncio
async def test_return_bad_request_delete_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_delete_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{999999999}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Review not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_delete_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    review_data = await create_review(user_data, enterprise_data, user_data_two)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{review_data.id}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == "Review deleted with successfully"
    assert data['code'] == 200

    assert body is None

@pytest.mark.asyncio
async def test_return_bad_request_get_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_get_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{999999999}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Review not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_get_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    review_data = await create_review(user_data, enterprise_data, user_data_two)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{review_data.id}", headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == "Review found with successfully"
    assert data['code'] == 200

    assert body['id'] == review_data.id
    assert body['user_id'] == review_data.user_id
    assert body['enterprise_id'] == review_data.enterprise_id

@pytest.mark.asyncio
async def test_not_exists_enterprise_create_review_in_enterprise():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    dto = CreateReviewEnterpriseDTO(
        rating = 5,
        title = "title any",
        description = ("description any" * 20),
        pros = None,
        cons = None,
        would_recommend = True,
        position = None,
        salary_range = None,
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        enterprise_id = 999999999
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    assert response.status_code == 404
    assert data['code'] == 404
    assert data['message'] == "Enterprise not found"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_employee_not_exists_create_review_in_enterprise():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    dto = CreateReviewEnterpriseDTO(
        rating = 5,
        title = "title any",
        description = ("description any" * 20),
        pros = None,
        cons = None,
        would_recommend = True,
        position = None,
        salary_range = None,
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        enterprise_id = enterprise_data.id
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    assert response.status_code == 404
    assert data['code'] == 404
    assert data['status'] == False
    assert data['message'] == "you are not or were not an employee"
    assert data['body'] == None

@pytest.mark.asyncio
async def test_exists_review_create_review_in_enterprise():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    review_data = await create_review(user_data, enterprise_data, user_data_two)

    dto = CreateReviewEnterpriseDTO(
        rating = 5,
        title = "title any",
        description = ("description any" * 20),
        pros = None,
        cons = None,
        would_recommend = True,
        position = None,
        salary_range = None,
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        enterprise_id = enterprise_data.id
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    assert response.status_code == 409
    assert data['code'] == 409
    assert data['status'] == False

@pytest.mark.asyncio
async def test_create_review_in_enterprise():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    dto = CreateReviewEnterpriseDTO(
        rating = 5,
        title = "title any",
        description = ("description any" * 20),
        pros = None,
        cons = None,
        would_recommend = True,
        position = None,
        salary_range = None,
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        enterprise_id = enterprise_data.id
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})

    data = response.json()
    print(data)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_all_review_enterprise():
    user_data: Final = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200