from dotenv import load_dotenv
from fastapi.testclient import TestClient
from typing import Final

from app.configs.commands.command_linner import ROLE_SUPER_ADM
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_category, create_post_user, \
    create_follow_user, \
    create_comment_post_user, create_industry, create_enterprise, create_post_enterprise, \
    create_follow_enterprise_user, create_area, create_vacancy, log_in_system, create_and_login_user_without_role
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import asyncio

load_dotenv()

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/notification"

@pytest.mark.asyncio
async def test_received_notification_about_new_system():
    adm_master = await log_in_system()
    user = await create_and_login_user_without_role()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            f"{"/api/v1/adm"}/toggle/{user.out.email}/{ROLE_SUPER_ADM}",
            headers={"Authorization": f"Bearer {adm_master.tokens.token}"}
        )

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user.out.id}",
            headers={"Authorization": f"Bearer {user.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) >= 1
    assert data['items'][0]['user_id'] == user.out.id
    assert data['items'][0]['entity_id'] is None
    assert data['items'][0]['title'] == f"Congratulations! You are the new {ROLE_SUPER_ADM}"

@pytest.mark.asyncio
async def test_received_notification_about_new_vacancy_enterprise():
    user_owner_enterprise = await create_and_login_user_with_role_super_adm()
    user_data_2: Final = await create_and_login_user_without_role()

    industry_data: Final = await create_industry(user_owner_enterprise)
    enterprise_data: Final = await create_enterprise(user_owner_enterprise, industry_data)
    area_data = await create_area(user_owner_enterprise)

    await create_follow_enterprise_user(user_owner_enterprise, user_data_2)

    vacancy_data = await create_vacancy(user_owner_enterprise, area_data)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data_2.out.id}",
            headers={"Authorization": f"Bearer {user_data_2.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) >= 1
    assert data['items'][0]['user_id'] == user_data_2.out.id
    assert data['items'][0]['entity_id'] == vacancy_data.id

@pytest.mark.asyncio
async def test_received_notification_about_new_post_enterprise():
    user_owner_enterprise = await create_and_login_user_with_role_super_adm()
    user_data_2 = await create_and_login_user_without_role()

    industry_data = await create_industry(user_owner_enterprise)
    enterprise_data = await create_enterprise(user_owner_enterprise, industry_data)
    category_data: Final = await create_category(user_owner_enterprise)

    await create_follow_enterprise_user(user_owner_enterprise, user_data_2)

    post_data = await create_post_enterprise(user_owner_enterprise, enterprise_data, category_data)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_data_2.out.id}",
            headers={"Authorization": f"Bearer {user_data_2.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert data['items'][0]['user_id'] == user_data_2.out.id
    assert data['items'][0]['entity_id'] == post_data.id

@pytest.mark.asyncio
async def test_sending_notification_about_new_follow():
    user_follower_A = await create_and_login_user_with_role_super_adm()
    user_followed_B = await create_and_login_user_with_role_super_adm()

    await create_follow_user(
        follower_data=user_follower_A,
        followed_data=user_followed_B
    )

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_followed_B.out.id}",
            headers={"Authorization": f"Bearer {user_followed_B.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert data['items'][0]['user_id'] == user_followed_B.out.id

@pytest.mark.asyncio
async def test_sending_notification_about_new_comment():
    user_follower_A = await create_and_login_user_with_role_super_adm()
    user_followed_B = await create_and_login_user_with_role_super_adm()

    await create_follow_user(
        follower_data=user_follower_A,
        followed_data=user_followed_B
    )

    category_data: Final = await create_category(user_followed_B)
    post_user_data: Final = await create_post_user(user_followed_B, category_data)
    comment_data = await create_comment_post_user(user_followed_B, post_user_data)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_follower_A.out.id}",
            headers={"Authorization": f"Bearer {user_follower_A.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert data['items'][0]['user_id'] == user_follower_A.out.id

@pytest.mark.asyncio
async def test_received_notification_by_new_post():
    user_follower_A = await create_and_login_user_with_role_super_adm()
    user_followed_B = await create_and_login_user_with_role_super_adm()

    await create_follow_user(
        follower_data=user_follower_A,
        followed_data=user_followed_B
    )

    category_data: Final = await create_category(user_followed_B)
    post_user_data: Final = await create_post_user(user_followed_B, category_data)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?user_id={user_follower_A.out.id}",
            headers={"Authorization": f"Bearer {user_follower_A.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) >= 1
    assert data['items'][0]['user_id'] == user_follower_A.out.id
