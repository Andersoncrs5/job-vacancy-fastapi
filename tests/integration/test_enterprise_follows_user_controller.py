from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, UserTestData, create_follow_user, create_industry, \
    create_enterprise, create_follow_enterprise_user
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.follow_schemas import *
import pytest

client: Final[TestClient] = TestClient(app)
URL = "/api/v1/enterprise-follow-user"


@pytest.mark.asyncio
async def test_exists_follow_user_status():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_to_follow: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(
            f'{URL}/exists?followed_user_id={user_to_follow.out.id}',
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['status'] == True
    assert data['body'] == False

    await create_follow_enterprise_user(user_data, user_to_follow)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.get(
            f'{URL}/exists?followed_user_id={user_to_follow.out.id}',
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['status'] == True
    assert data['body'] == True

@pytest.mark.asyncio
async def test_get_all_follows_with_filter():
    user_a: Final = await create_and_login_user()
    industry_a: Final = await create_industry(user_a)
    enterprise_a: Final = await create_enterprise(user_a, industry_a)

    user_b_data: Final = await create_and_login_user()
    user_c: Final = await create_and_login_user()

    await create_follow_enterprise_user(user_a, user_b_data)
    await create_follow_enterprise_user(user_a, user_c)

    auth_header = {"Authorization": f"Bearer {user_a.tokens.token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:

        response_all = await acdc.get(URL, headers=auth_header)

        assert response_all.status_code == 200
        data_all = response_all.json()
        assert data_all['total']

@pytest.mark.asyncio
async def test_bad_request_follow_user():
    user_data: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f'{URL}/toggle/{0}',
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"Id is required"
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_follow_user():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f'{URL}/toggle/{user_data_two.out.id}',
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You are following the user {user_data_two.out.name}"
    assert data['status'] == True

    assert body is None

@pytest.mark.asyncio
async def test_delete_follow_user():
    user_data: Final = await create_and_login_user()
    industry_data: Final = await create_industry(user_data)
    enterprise_data: Final = await create_enterprise(user_data, industry_data)

    user_data_two: Final = await create_and_login_user()
    await create_follow_enterprise_user(user_data, user_data_two)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f'{URL}/toggle/{user_data_two.out.id}',
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You unfollowed the user {user_data_two.out.name}"
    assert data['status'] == True

    assert body is None
