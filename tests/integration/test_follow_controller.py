from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, UserTestData, create_follow_user
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.follow_schemas import *
import pytest

client: Final[TestClient] = TestClient(app)
URL: Final[str] = "/api/v1/follow"

@pytest.mark.asyncio
async def test_return_bad_request_exists_follow():
    user_data = await create_and_login_user_with_role_super_adm()

    followed_data_1 = await create_and_login_user_with_role_super_adm()
    await create_follow_user(user_data, followed_data_1)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data_2 = response.json()

    assert response.status_code == 400
    assert data_2['code'] == 400
    assert data_2['message'] == 'Id is required'

@pytest.mark.asyncio
async def test_check_exists_follow():
    user_data = await create_and_login_user_with_role_super_adm()

    followed_data_1 = await create_and_login_user_with_role_super_adm()
    await create_follow_user(user_data, followed_data_1)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{followed_data_1.out.id}/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data_2 = response.json()
    body_2 = response.json()['body']

    assert response.status_code == 200

    assert body_2 == True

@pytest.mark.asyncio
async def test_return_bad_request_delete_follow():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']

    assert response.status_code == 400

    assert data['message'] == f"Id is required"
    assert data['code'] == 400
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_delete_follow():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{99999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']

    assert response.status_code == 404

    assert data['message'] == f"User not found"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_delete_follow():
    user_data = await create_and_login_user_with_role_super_adm()

    followed_data_1 = await create_and_login_user_with_role_super_adm()
    await create_follow_user(user_data, followed_data_1)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{followed_data_1.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']

    assert response.status_code == 200

    assert data['message'] == f"you unfollowed {followed_data_1.out.name}"
    assert data['code'] == 200
    assert data['status'] == True

    assert body is None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response_2: Final = await acdc.get(
            f"{URL}/{followed_data_1.out.id}/exists",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data_2 = response_2.json()
    body_2 = response_2.json()['body']

    assert response_2.status_code == 200

    assert body_2 == False

@pytest.mark.asyncio
async def test_return_bad_request_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']

    assert response.status_code == 400

    assert data['message'] == 'Id is required'
    assert data['status'] == False
    assert data['code'] == 400

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_get_all():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{9999999}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']

    assert response.status_code == 404

    assert data['message'] == 'User not found'
    assert data['status'] == False
    assert data['code'] == 404

    assert body is None

@pytest.mark.asyncio
async def test_get_all():
    user_data = await create_and_login_user_with_role_super_adm()
    followed_data_1 = await create_and_login_user_with_role_super_adm()
    followed_data_2 = await create_and_login_user_with_role_super_adm()
    followed_data_3 = await create_and_login_user_with_role_super_adm()

    await create_follow_user(user_data, followed_data_1)
    await create_follow_user(user_data, followed_data_2)
    await create_follow_user(user_data, followed_data_3)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{user_data.out.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    followed = data['items'][0]

    assert followed['followed_id'] == followed_data_3.out.id

@pytest.mark.asyncio
async def test_conflict_already_follow():
    follower_data: UserTestData = await create_and_login_user_with_role_super_adm()
    followed_data: UserTestData = await create_and_login_user_with_role_super_adm()
    await create_follow_user(follower_data, followed_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{followed_data.out.id}",
            headers={"Authorization": f"Bearer {follower_data.tokens.token}"}
        )

    assert response.status_code == 409
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You already are following the {followed_data.out.name}"
    assert data['code'] == 409
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_return_bad_request_follow_create():
    follower_data: UserTestData = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{0}",
            headers={"Authorization": f"Bearer {follower_data.tokens.token}"}
        )

    assert response.status_code == 400
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"Id is required"
    assert data['code'] == 400
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_return_not_found_follow_create():
    follower_data: UserTestData = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{999999999}",
            headers={"Authorization": f"Bearer {follower_data.tokens.token}"}
        )

    assert response.status_code == 404
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"User not found"
    assert data['code'] == 404
    assert data['status'] == False

    assert body is None

@pytest.mark.asyncio
async def test_follow_create():
    follower_data: UserTestData = await create_and_login_user_with_role_super_adm()
    followed_data: UserTestData = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{followed_data.out.id}",
            headers={"Authorization": f"Bearer {follower_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You are following the {followed_data.out.name}"

    assert body is None
