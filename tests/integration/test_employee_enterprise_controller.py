from fastapi.testclient import TestClient
from typing import Final
from app.schemas.employee_enterprise_schemas import *
from tests.integration.helper import create_and_login_user, create_industry, create_enterprise, create_employee
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from datetime import date
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/employee-enterprise'

@pytest.mark.asyncio
async def test_patch_employee_successfully():
    user_data: Final = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    user_data_two: Final = await create_and_login_user()
    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    dto = UpdateEmployeeEnterpriseDTO(
        position="Senior Software Engineer",
        salary_range="8000-12000",
        employment_type=EmploymentTypeEnum.contract,
        employment_status=EmploymentStatusEnum.on_leave,
        start_date=date.today(),
        end_date=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{employee_data.id}",
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Employee updated with successfully"
    assert data['code'] == 200
    assert data['status'] is True
    assert data['body'] is not None
    assert data['body']['id'] == employee_data.id
    assert data['body']['position'] == dto.position
    assert data['body']['salary_range'] == dto.salary_range
    assert data['body']['employment_type'] == dto.employment_type
    assert data['body']['employment_status'] == dto.employment_status

@pytest.mark.asyncio
async def test_patch_employee_bad_request():
    user_data: Final = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    user_data_two: Final = await create_and_login_user()
    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    dto = UpdateEmployeeEnterpriseDTO(
        position="QA Engineer",
        salary_range="3000-5000",
        employment_type=EmploymentTypeEnum.part_time,
        employment_status=EmploymentStatusEnum.probation,
        start_date=date.today(),
        end_date=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}",
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] is False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_patch_employee_not_found():
    user_data: Final = await create_and_login_user()
    industry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, industry_data)
    user_data_two: Final = await create_and_login_user()
    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    dto = UpdateEmployeeEnterpriseDTO(
        position="DevOps Engineer",
        salary_range="10000-15000",
        employment_type=EmploymentTypeEnum.full_time,
        employment_status=EmploymentStatusEnum.vacation,
        start_date=date.today(),
        end_date=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{9999999999}",
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data['message'] == "Employee not found"
    assert data['code'] == 404
    assert data['status'] is False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{employee_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Employee deleted with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_delete_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_delete_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{9999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Employee not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{9999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Employee not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{employee_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Employee found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is not None
    assert data['body']['id'] == employee_data.id
    assert data['body']['user_id'] == employee_data.user_id
    assert data['body']['enterprise_id'] == employee_data.enterprise_id

@pytest.mark.asyncio
async def test_return_conflict_user_enterprise_create_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    dto = CreateEmployeeEnterpriseDTO(
        user_id = user_data.out.id,
        position = "SOFTWARE ENGINEER",
        salary_range = "5000-8000",
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        start_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 409

    assert data['message'] == "You cannot add yourself"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_user_create_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    dto = CreateEmployeeEnterpriseDTO(
        user_id = 9999999999999,
        position = "SOFTWARE ENGINEER",
        salary_range = "5000-8000",
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        start_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "User not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_conflict_create_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two, URL)

    dto = CreateEmployeeEnterpriseDTO(
        user_id = employee_data.user_id,
        position = "SOFTWARE ENGINEER",
        salary_range = "5000-8000",
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        start_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 409

    assert data['message'] == "User already exists"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_create_employee():
    user_data: Final = await create_and_login_user()
    inudstry_data = await create_industry(user_data)
    enterprise_data = await create_enterprise(user_data, inudstry_data)

    user_data_two: Final = await create_and_login_user()

    dto = CreateEmployeeEnterpriseDTO(
        user_id = user_data_two.out.id,
        position = "SOFTWARE ENGINEER",
        salary_range = "5000-8000",
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        start_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Employee created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']["id"] is not None
    assert data['body']["user_id"] == dto.user_id
    assert data['body']["position"] == dto.position
    assert data['body']["salary_range"] == dto.salary_range

@pytest.mark.asyncio
async def test_get_all_enterprise():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(f'{URL}', headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200