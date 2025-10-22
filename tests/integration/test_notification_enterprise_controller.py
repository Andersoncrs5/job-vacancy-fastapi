from fastapi.testclient import TestClient
from typing import Final

from app.dependencies.service_dependency import get_follow_service_provider_dependency
from app.schemas.category_schemas import *
from app.schemas.follow_schemas import UpdateFollowDTO
from app.services.providers.follow_service_provider import FollowServiceProvider
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_category, create_post_user, create_follow_user, \
    create_comment_post_user, create_industry, create_enterprise, create_post_enterprise, create_follow_enterprise, \
    create_follow_enterprise_user, create_area, create_vacancy, create_employee, create_review, UserTestData, \
    create_application
from main import app
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from httpx import ASGITransport, AsyncClient
import pytest
import asyncio

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/notification-enterprise"

@pytest.mark.asyncio
async def test_received_notify_about_new_application():
    user_data: UserTestData = await create_and_login_user_with_role_super_adm()
    user_data_two: UserTestData = await create_and_login_user_with_role_super_adm()

    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)
    area_data = await create_area(user_data)
    vacancy_data = await create_vacancy(user_data, area_data)
    application = await create_application(user_data_two, vacancy_data)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?enterprise_id={enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) >= 1
    assert data['items'][0]['enterprise_id'] == enterprise_data.id
    assert data['items'][0]['entity_id'] == application.id

@pytest.mark.asyncio
async def test_received_notify_about_new_review():
    user_data: Final = await create_and_login_user_with_role_super_adm()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user_with_role_super_adm()

    employee_data = await create_employee(user_data, enterprise_data, user_data_two)

    review_data = await create_review(user_data, enterprise_data, user_data_two)

    await asyncio.sleep(4)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.get(
            f"{URL}?enterprise_id={enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) >= 1
    assert data['items'][0]['enterprise_id'] == enterprise_data.id
    assert data['items'][0]['entity_id'] == review_data.id
