from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_curriculum
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from app.schemas.curriculum_schemas import *

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/curriculum'

@pytest.mark.asyncio
async def test_update_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    dto = UpdateCurriculumDTO(
        title = "updated",
        is_updated = True,
        is_visible = True,
        description = "desc update",
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Curriculum updated with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is not None
    assert data['body']['id'] == curriculum_data.id
    assert data['body']['user_id'] == curriculum_data.user_id
    assert data['body']['title'] == dto.title
    assert data['body']['is_updated'] == dto.is_updated
    assert data['body']['description'] == dto.description

@pytest.mark.asyncio
async def test_toggle_is_updated_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(f"{URL}/toggle/status/is_updated", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Curriculum status is updated changed with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is not None
    assert data['body']['id'] == curriculum_data.id
    assert data['body']['user_id'] == curriculum_data.user_id

@pytest.mark.asyncio
async def test_delete_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(f"{URL}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Curriculum deleted with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_not_found_get_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{99999999999999999}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 404

    assert data['message'] == "Curriculum not found"
    assert data['code'] == 404
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_bad_request_get_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{0}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 400

    assert data['message'] == "Id is required"
    assert data['code'] == 400
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_return_forb_get_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_two = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    dto = UpdateCurriculumDTO(
        title=None,
        is_updated=None,
        is_visible=False,
        description=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        await acdc.get(f"{URL}/{curriculum_data.user_id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})


        await acdc.patch(f"{URL}", json=dict(dto),
                                           headers={"Authorization": f"Bearer {user_data.tokens.token}"})

        response: Final = await acdc.get(f"{URL}/{user_data.out.id}",
                                         headers={"Authorization": f"Bearer {user_data_two.tokens.token}"})


    data = response.json()
    assert response.status_code == 403

    assert data['message'] == "Curriculum cannot be accessed"
    assert data['code'] == 403
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_get_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(f"{URL}/{curriculum_data.user_id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 200

    assert data['message'] == "Curriculum found with successfully"
    assert data['code'] == 200
    assert data['status'] == True
    assert data['body'] is not None
    assert data['body']['id'] == curriculum_data.id
    assert data['body']['user_id'] == curriculum_data.user_id

@pytest.mark.asyncio
async def test_conflict_create_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()
    curriculum_data = await create_curriculum(user_data)

    dto = CreateCurriculumDTO(
        title = "a little about me",
        description = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 409

    assert data['message'] == "you already have a Curriculum"
    assert data['status'] == False
    assert data['body'] is None

@pytest.mark.asyncio
async def test_create_curriculum():
    user_data = await create_and_login_user_with_role_super_adm()

    dto = CreateCurriculumDTO(
        title = "a little about me",
        description = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Curriculum created with successfully"
    assert data['code'] == 201
    assert data['body']['id'] is not None
    assert data['body']['user_id'] is not None
    assert data['body']['title'] == dto.title
