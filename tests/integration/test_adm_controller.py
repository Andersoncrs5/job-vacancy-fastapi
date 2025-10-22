import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_area, log_in_system, \
    impl_role_in_user, create_and_login_user_without_role
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.area_schemas import *
import pytest
import random

load_dotenv()

ROLE_SUPER_ADM: Final[str] = os.getenv("ROLE_SUPER_ADM")
ROLE_ADM: Final[str] = os.getenv("ROLE_ADM")
ROLE_MASTER: Final[str] = os.getenv("ROLE_MASTER")

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/adm'

@pytest.mark.asyncio
async def test_return_unauthorized_get_all():
    user = await create_and_login_user_without_role()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}",
            headers={"Authorization": f"Bearer {user.tokens.token}"}
        )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_all():
    user = await log_in_system()
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"{URL}?user_id={user_data.out.id}",
            headers={"Authorization": f"Bearer {user.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    items = list(data['items'])

    assert items[0]['user_id'] == user_data.out.id

@pytest.mark.asyncio
async def test_role_not_exists_adm_in_user():
    adm_master = await log_in_system()
    user = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"{URL}/toggle/{user.out.email}/{"ROLE_POKEMON"}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    assert response.status_code == 404

    data = response.json()
    body = response.json()["body"]

    assert data['message'] == f"The role {"ROLE_POKEMON"} is not {ROLE_SUPER_ADM} or {ROLE_ADM}"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_remove_role_adm_in_user():
    adm_master = await log_in_system()
    user = await create_and_login_user_with_role_super_adm()
    await impl_role_in_user(user.out.email, user.out.name, ROLE_ADM)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"{URL}/toggle/{user.out.email}/{ROLE_ADM}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()["body"]

    assert data['message'] == f"User {user.out.name} not a more a {ROLE_ADM.lower()}"
    assert data['code'] == 200
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_remove_role_super_adm_in_user():
    adm_master = await log_in_system()
    user = await create_and_login_user_with_role_super_adm()
    await impl_role_in_user(user.out.email, user.out.name, ROLE_ADM)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"{URL}/toggle/{user.out.email}/{ROLE_SUPER_ADM}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()["body"]

    assert data['message'] == f"User {user.out.name} not a more a {ROLE_SUPER_ADM.lower()}"
    assert data['code'] == 200
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_add_role_adm_in_user():
    adm_master = await log_in_system()
    user = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"{URL}/toggle/{user.out.email}/{ROLE_ADM}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()["body"]

    assert data['message'] == f"User {user.out.name} now is a {ROLE_ADM.lower()}"
    assert data['code'] == 200
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_add_role_super_adm_in_user():
    adm_master = await log_in_system()
    user = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"{URL}/toggle/{user.out.email}/{ROLE_SUPER_ADM}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    assert response.status_code == 200

    data = response.json()
    body = response.json()["body"]

    assert data['message'] == f"User {user.out.name} now is a {ROLE_SUPER_ADM.lower()}"
    assert data['code'] == 200
    assert data['status'] == True

    assert body is None