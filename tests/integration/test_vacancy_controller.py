from fastapi.testclient import TestClient
from typing import Final
from app.schemas.enterprise_schemas import *
from tests.integration.helper import create_and_login_user, create_industry, create_enterprise, create_area, create_vacancy
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from app.schemas.vacancy_schemas import *
from app.configs.db.enums import (
    MediaType, EmploymentTypeEnum, 
    EmploymentStatusEnum, ExperienceLevelEnum, EducationLevelEnum, 
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum
)

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/vacancy'

@pytest.mark.asyncio
async def test_return_bad_request_patch_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    dto = UpdateVacancyDTO(
        area_id =  None,
        title =  "Vacancy any",
        description =  None,
        employment_type =  None,
        experience_level =  None,
        education_level =  None,
        workplace_type =  None,
        seniority =  None,
        salary_min =  None,
        salary_max =  None,
        currency =  None,
        requirements =  None,
        responsibilities =  None,
        benefits =  None,
        status =  None,
        openings =  None,
        application_deadline =  None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_patch_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    dto = UpdateVacancyDTO(
        area_id =  None,
        title =  "Vacancy any",
        description =  None,
        employment_type =  None,
        experience_level =  None,
        education_level =  None,
        workplace_type =  None,
        seniority =  None,
        salary_min =  None,
        salary_max =  None,
        currency =  None,
        requirements =  None,
        responsibilities =  None,
        benefits =  None,
        status =  None,
        openings =  None,
        application_deadline =  None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{9999999}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Vacancy not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_patch_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    dto = UpdateVacancyDTO(
        area_id =  None,
        title =  "Vacancy any",
        description =  None,
        employment_type =  None,
        experience_level =  None,
        education_level =  None,
        workplace_type =  None,
        seniority =  None,
        salary_min =  None,
        salary_max =  None,
        currency =  None,
        requirements =  None,
        responsibilities =  None,
        benefits =  None,
        status =  None,
        openings =  None,
        application_deadline =  None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{vacancy_data.id}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == "Vacancy updated with successfully"
    assert data['code'] == 200

    assert body is not None
    assert body['id'] == vacancy_data.id
    assert body['enterprise_id'] == vacancy_data.enterprise_id
    assert body['title'] == dto.title

@pytest.mark.asyncio
async def test_get_all_vacancy():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_return_bad_request_delete_vacancy():
    user_data: Final = await create_and_login_user()
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_delete_vacancy():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{9999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Vacancy not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_delete_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{vacancy_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == "Vacancy deleted with successfully"
    assert data['code'] == 200

    assert body is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_two: Final = await acdc.delete(f"{URL}/{vacancy_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data_two = response_two.json()
    body_two = response_two.json()['body']
    assert response_two.status_code == 404

    assert data_two['message'] == "Vacancy not found"
    assert data_two['code'] == 404
    
@pytest.mark.asyncio
async def test_return_bad_request_get_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_get_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{9999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Vacancy not found"
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_get_vacancy():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{vacancy_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == "Vacancy found with successfully"
    assert data['code'] == 200

    assert body is not None
    assert body['id'] == vacancy_data.id
    assert body['enterprise_id'] == vacancy_data.enterprise_id
    assert body['title'] == vacancy_data.title

@pytest.mark.asyncio
async def test_return_not_found_enterprise_create_vacancy_success():
    user_data: Final = await create_and_login_user()
    area_data = await create_area(user_data)

    dto = CreateVacancyDTO(
        area_id = area_data.id,
        title = "New vacancy",
        description = "Des of vacancy",
        employment_type = EmploymentTypeEnum.full_time,
        experience_level = ExperienceLevelEnum.INTERN,
        education_level = EducationLevelEnum.MASTER,
        workplace_type = WorkplaceTypeEnum.REMOTE,
        seniority = None,
        salary_min = None,
        salary_max = None,
        currency = "USD",
        requirements = None,
        responsibilities = None,
        benefits = None,
        status = VacancyStatusEnum.OPEN,
        openings = 1,
        application_deadline = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(URL, 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()

    assert response.status_code == 404
    assert data["message"] == "Enterprise not found"
    assert data["code"] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_area_create_vacancy_success():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    dto = CreateVacancyDTO(
        area_id = 99999999,
        title = "New vacancy",
        description = "Des of vacancy",
        employment_type = EmploymentTypeEnum.full_time,
        experience_level = ExperienceLevelEnum.INTERN,
        education_level = EducationLevelEnum.MASTER,
        workplace_type = WorkplaceTypeEnum.REMOTE,
        seniority = None,
        salary_min = None,
        salary_max = None,
        currency = "USD",
        requirements = None,
        responsibilities = None,
        benefits = None,
        status = VacancyStatusEnum.OPEN,
        openings = 1,
        application_deadline = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(URL, 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()

    assert response.status_code == 404
    assert data["message"] == "Area not found"
    assert data["code"] == 404
    assert data['body'] is None
    
@pytest.mark.asyncio
async def test_create_vacancy_success():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)

    dto = CreateVacancyDTO(
        area_id = area_data.id,
        title = "New vacancy",
        description = "Des of vacancy",
        employment_type = EmploymentTypeEnum.full_time,
        experience_level = ExperienceLevelEnum.INTERN,
        education_level = EducationLevelEnum.MASTER,
        workplace_type = WorkplaceTypeEnum.REMOTE,
        seniority = None,
        salary_min = None,
        salary_max = None,
        currency = "USD",
        requirements = None,
        responsibilities = None,
        benefits = None,
        status = VacancyStatusEnum.OPEN,
        openings = 1,
        application_deadline = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(URL, 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()

    assert response.status_code == 201
    assert data["message"] == "Vacancy created with successfully"
    assert data["code"] == 201
    assert data['body']['id'] is not None
    assert data['body']['area_id'] == dto.area_id
    assert data['body']['enterprise_id'] == enterprise_data.id
    assert data['body']['title'] == dto.title
    