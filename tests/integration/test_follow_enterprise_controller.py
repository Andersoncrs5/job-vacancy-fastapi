from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, create_industry, create_enterprise, \
    create_follow_enterprise
from main import app
from httpx import ASGITransport, AsyncClient
import pytest

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/follow-enterprise"

@pytest.mark.asyncio
async def test_delete_follow_enterprise_bad_request():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/0",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()

    assert data['message'] == "Id is required"
    assert data['status'] is False
    assert data['code'] == 400
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_follow_enterprise_not_found():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()

    assert data['message'] == "You are not following this enterprise"
    assert data['status'] is False
    assert data['code'] == 404
    assert data['body'] is None

@pytest.mark.asyncio
async def test_delete_follow_enterprise_success():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)
    await create_follow_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert data['status'] is True
    assert data['code'] == 200
    assert data['body'] is None

@pytest.mark.asyncio
async def test_exists_bad_request():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/0/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = data['body']

    assert data['message'] == "Id is required"
    assert data['status'] is False
    assert data['code'] == 400
    assert body is None

@pytest.mark.asyncio
async def test_exists_return_true_when_user_follows_enterprise():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)

    await create_follow_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{enterprise_data.id}/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = data['body']

    assert data['status'] is True
    assert data['code'] == 200
    assert isinstance(body, bool)
    assert body is True

@pytest.mark.asyncio
async def test_exists_return_false_when_user_not_follows_enterprise():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)


    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{enterprise_data.id}/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()
    body = data['body']

    assert data['status'] is True
    assert data['code'] == 200
    assert isinstance(body, bool)
    assert body is False

@pytest.mark.asyncio
async def test_return_null_ids_get_all():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == 'You must provide either user_id or enterprise_id, not both.'
    assert data['status'] == False
    assert data['code'] == 400
    assert body is None

@pytest.mark.asyncio
async def test_return_2_ids_get_all():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}?user_id={user_data.out.id}&enterprise_id={enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == 'You must provide either user_id or enterprise_id, not both.'
    assert data['status'] == False
    assert data['code'] == 400
    assert body is None

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)
    await create_follow_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}?user_id={user_data.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 200
    data = response.json()

    assert data['items'] is not None
    user = data['items'][0]
    assert user['user_id'] == user_data.out.id
    assert user['follower']['id'] == user['user_id']

@pytest.mark.asyncio
async def test_bad_request_follow_enterprise():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"Id is required"
    assert data['code'] == 400
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_not_found_follow_enterprise():
    user_data = await create_and_login_user()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{999999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"Enterprise not found"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_exists_create_follow_enterprise():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)
    await create_follow_enterprise(user_data, enterprise_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 409
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You already are following the enterprise: {enterprise_data.name}"
    assert data['code'] == 409
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_follow_self_enterprise_create_follow_enterprise():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data_2.tokens.token}"}
        )

    assert response.status_code == 403
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You cannot to follow your enterprise!"
    assert data['code'] == 403
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_create_follow_enterprise():
    user_data = await create_and_login_user()

    user_data_2 = await create_and_login_user()
    industry_data = await create_industry(user_data_2)
    enterprise_data = await create_enterprise(user_data_2, industry_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You are following the enterprise {enterprise_data.name}"
    assert data['code'] == 201
    assert data['status'] == True

    assert body is None