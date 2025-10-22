from fastapi.testclient import TestClient
from typing import Final
from app.schemas.enterprise_schemas import *
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_industry, create_enterprise, create_area, create_vacancy, create_skill, add_skill_into_vacancy
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from app.schemas.vacancy_schemas import *
from app.schemas.vacancy_skill_schemas import CreateVacancySkillDTO, UpdateVacancySkillDTO
from app.configs.db.enums import (
    MediaType, EmploymentTypeEnum, ProficiencyEnum,
    EmploymentStatusEnum, ExperienceLevelEnum, EducationLevelEnum, 
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum
)

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/vacancy-skill'


@pytest.mark.asyncio
async def test_get_return_bad_request_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == 'Id is required'

    assert body is None

@pytest.mark.asyncio
async def test_get_return_not_found_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{9999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == 'Skill not found'

    assert body is None

@pytest.mark.asyncio
async def test_delete_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{vs_data}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == 'Skill found with successfully'

    assert body is not None
    assert body['id'] == vs_data

@pytest.mark.asyncio
async def test_patch_return_bad_request_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = UpdateVacancySkillDTO(
        is_required = None,
        proficiency = None,
        years_experience = None,
        priority_level = None,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == 'Id is required'

    assert body is None

@pytest.mark.asyncio
async def test_patch_return_not_found_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = UpdateVacancySkillDTO(
        is_required = None,
        proficiency = None,
        years_experience = None,
        priority_level = None,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{9999999}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == 'Skill not found'

    assert body is None

@pytest.mark.asyncio
async def test_patch_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = UpdateVacancySkillDTO(
        is_required = False,
        proficiency = None,
        years_experience = 4,
        priority_level = 8,
        notes = "Note updated",
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{vs_data}", 
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == 'Skill details updated with successfully'

    assert body is None

@pytest.mark.asyncio
async def test_return_bad_request_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}/all", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == "Id is required"

@pytest.mark.asyncio
async def test_return_not_found_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{99999999}/all", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == "Vacancy not found"

@pytest.mark.asyncio
async def test_get_all_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)

    skill_data = await create_skill(user_data)
    skill_data_two = await create_skill(user_data)
    skill_data_thirt = await create_skill(user_data)

    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)
    vs_data_2 = await add_skill_into_vacancy(user_data, vacancy_data, skill_data_two)
    vs_data_3 = await add_skill_into_vacancy(user_data, vacancy_data, skill_data_thirt)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{vacancy_data.id}/all", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['items'] is not None
    assert data['total'] is not None
    assert data['page'] is not None
    assert data['size'] is not None
    assert data['pages'] is not None

@pytest.mark.asyncio
async def test_delete_return_bad_request_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{0}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 400

    assert data['message'] == 'Id is required'

    assert body is None

@pytest.mark.asyncio
async def test_delete_return_not_found_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{9999999}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == 'Skill not found'

    assert body is None

@pytest.mark.asyncio
async def test_delete_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{vs_data}", 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 200

    assert data['message'] == 'Skill removed with successfully'

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_skill_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = CreateVacancySkillDTO(
        vacancy_id = vacancy_data.id,
        skill_id = 99999999,
        is_required = True,
        proficiency = ProficiencyEnum.basic,
        years_experience = 2,
        priority_level = 3,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == 'Skill not found'

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_vacancy_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = CreateVacancySkillDTO(
        vacancy_id = 9999999,
        skill_id = skill_data.id,
        is_required = True,
        proficiency = ProficiencyEnum.basic,
        years_experience = 2,
        priority_level = 3,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 404

    assert data['message'] == 'Vacancy not found'

    assert body is None

@pytest.mark.asyncio
async def test_error_exists_skill_in_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)
    vs_data = await add_skill_into_vacancy(user_data, vacancy_data, skill_data)

    dto = CreateVacancySkillDTO(
        vacancy_id = vacancy_data.id,
        skill_id = skill_data.id,
        is_required = True,
        proficiency = ProficiencyEnum.basic,
        years_experience = 2,
        priority_level = 3,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 409

    assert data['message'] == 'Skill already was added'

    assert body is None

@pytest.mark.asyncio
async def test_create_skill_to_vacancy():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    skill_data = await create_skill(user_data)

    dto = CreateVacancySkillDTO(
        vacancy_id = vacancy_data.id,
        skill_id = skill_data.id,
        is_required = True,
        proficiency = ProficiencyEnum.basic,
        years_experience = 2,
        priority_level = 3,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 201

    assert data['message'] == 'Skill added with sucessfully'

    assert body is not None
    assert isinstance(body, int) == True