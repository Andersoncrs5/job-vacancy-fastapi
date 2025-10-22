from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_skill, \
    create_and_login_user_without_role
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.skill_schemas import *
import pytest
import random

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/skill'

@pytest.mark.asyncio
async def test_exists_name_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{skill_data.name}/exists", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['code'] == 200
    assert data['body'] == True

@pytest.mark.asyncio
async def test_toggle_is_active_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.put(f"{URL}/{skill_data.id}/toggle/status/active", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Skill updated status is active with successfully"
    assert data['code'] == 200
    assert data['body']['id'] == skill_data.id
    assert data['body']['name'] == skill_data.name
    assert data['body']['is_active'] != skill_data.is_active

@pytest.mark.asyncio
async def test_return_unauthorized_toggle_is_active_skill():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    user_data_no_roles: Final = await create_and_login_user_without_role()

    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.put(
            f"{URL}/{skill_data.id}/toggle/status/active",
            headers={"Authorization": f"Bearer {user_data_no_roles.tokens.token}"}
        )

    data = response.json()

    assert data["code"] == 401
    assert data["message"] == "You are not authorized"
    assert data["status"] == False

@pytest.mark.asyncio
async def test_return_unauthorized_skill():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    user_data_no_roles: Final = await create_and_login_user_without_role()

    skill_data = await create_skill(user_data)
    num = random.randint(10000,100000000000000)

    dto = UpdateSkillDTO(
        name = f"name {num}" ,
        is_active = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.put(
            f"{URL}/{skill_data.id}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_no_roles.tokens.token}"}
        )

    data = response.json()

    assert data["code"] == 401
    assert data["message"] == "You are not authorized"
    assert data["status"] == False

@pytest.mark.asyncio
async def test_update_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)
    num = random.randint(10000,100000000000000)

    dto = UpdateSkillDTO(
        name = f"name {num}" ,
        is_active = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.put(f"{URL}/{skill_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})


    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Skill updated with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body']['id'] == skill_data.id
    assert data['body']['is_active'] == skill_data.is_active
    assert data['body']['name'] == dto.name

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_return_not_found_delete_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{9999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Skill not found"
    assert data['code'] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_unauthorized_delete_skill():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    user_data_no_roles: Final = await create_and_login_user_without_role()

    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{skill_data.id}",
            headers={"Authorization": f"Bearer {user_data_no_roles.tokens.token}"}
        )

    data = response.json()
    assert data["code"] == 401
    assert data["message"] == "You are not authorized"
    assert data["status"] == False

@pytest.mark.asyncio
async def test_delete_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}/{skill_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Skill deleted with successfully"
    assert data['code'] == 200
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_skill():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{99999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Skill not found"
    assert data['code'] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    skill_data = await create_skill(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{skill_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Skill found with successfully"
    assert data['code'] == 200
    assert data['body']['id'] == skill_data.id
    assert data['body']['name'] == skill_data.name

@pytest.mark.asyncio
async def test_create_skill():
    user_data = await create_and_login_user_with_role_super_adm()
    num = random.randint(10000,100000000000000)

    dto = CreateSkillDTO(
        name = f"name {num}" 
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})


    data = response.json()
    assert response.status_code == 201