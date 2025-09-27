from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, create_skill, create_my_skill
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.my_skill_schemas import *
import pytest
import random
from uuid import UUID, uuid4
from app.configs.db.enums import ProficiencyEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/my-skill'

@pytest.mark.asyncio
async def test_return_bad_requests_exists_my_skil():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_false_exists_my_skil():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{999999999999}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == ""
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] == False

@pytest.mark.asyncio
async def test_return_true_existsexists_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{my_skill_data.skill_id}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == ""
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] == True


@pytest.mark.asyncio
async def test_return_bad_requests_get_my_skil():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_not_found_get_my_skil():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "My Skill not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_get_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{my_skill_data.skill_id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "My Skill found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body']['skill_id'] == my_skill_data.skill_id
    assert data['body']['proficiency'] == my_skill_data.proficiency
    assert data['body']['certificate_url'] == my_skill_data.certificate_url
    assert data['body']['datails'] == my_skill_data.datails
    assert data['body']['years_of_experience'] == my_skill_data.years_of_experience

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_return_bad_requests_update_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    dto = UpdateMySkillDTO(
        proficiency = ProficiencyEnum.intermediary,
        certificate_url = None,
        datails = "THE CHAINSAW DEMON",
        years_of_experience = 8,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{0}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_not_found_update_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    dto = UpdateMySkillDTO(
        proficiency = ProficiencyEnum.intermediary,
        certificate_url = None,
        datails = "THE CHAINSAW DEMON",
        years_of_experience = 8,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{999999999999}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "My Skill not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_update_my_skill():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    dto = UpdateMySkillDTO(
        proficiency = ProficiencyEnum.intermediary,
        certificate_url = None,
        datails = "THE CHAINSAW DEMON",
        years_of_experience = 8,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/{my_skill_data.skill_id}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "My Skill updated with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] != None
    assert data['body']['proficiency'] == dto.proficiency
    assert data['body']['datails'] == dto.datails
    assert data['body']['years_of_experience'] == dto.years_of_experience
    assert data['body']['skill_id'] == my_skill_data.skill_id
    assert data['body']['user_id'] == my_skill_data.user_id

@pytest.mark.asyncio
async def test_return_not_found_delete_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{99999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "My Skill not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_bad_request_delete_my_skil():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_delete_my_skill():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{skill_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "My Skill removed with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_not_found_create_my_skill():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    dto = CreateMySkillDTO(
        skill_id = 99999999999,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Skill not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_return_create_my_skill():
    user_data = await create_and_login_user()
    skill_data = await create_skill(user_data)
    my_skill_data = await create_my_skill(user_data, skill_data)

    dto = CreateMySkillDTO(
        skill_id = skill_data.id,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 409

    assert data['message'] == "Skill already was added"
    assert data['code'] == 409
    assert data['status'] == False
    assert data['body'] == None

@pytest.mark.asyncio
async def test_create_my_skill():
    user_data = await create_and_login_user()
    skill = await create_skill(user_data)

    dto = CreateMySkillDTO(
        skill_id = skill.id,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201    

    assert data['body']['skill_id'] == dto.skill_id
    assert data['body']['proficiency'] == dto.proficiency
    assert data['body']['certificate_url'] == dto.certificate_url
    assert data['body']['datails'] == dto.datails
    assert data['body']['years_of_experience'] == dto.years_of_experience