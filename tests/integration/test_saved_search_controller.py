from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user_with_role_super_adm, create_saved_search
from main import app
from httpx import ASGITransport, AsyncClient
import pytest
import random
from app.schemas.saved_search_schemas import *
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, UpdateSavedSearchDTO

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/saved-search'

@pytest.mark.asyncio
async def test_return_bad_request_patch_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    dto = {
        "name": "new name",
        "query": {"term": "developer"},
        "description": "updated description",
        "is_public": True,
        "last_executed_at": None,
        "notifications_enabled": True
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.patch(
            f"{URL}/{0}",
            json=dto,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400
    assert data["body"] is None
    assert data["code"] == 400
    assert data["message"] == "Id is required"
    assert data["status"] is False

@pytest.mark.asyncio
async def test_return_not_found_patch_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    dto = UpdateSavedSearchDTO(
        name = None,
        query = dict({"name": "new name"}),
        description = None,
        is_public = None,
        last_executed_at = None,
        notifications_enabled = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.patch(
            f"{URL}/{999999999}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404
    assert data["body"] is None
    assert data["code"] == 404
    assert data["message"] == "Search not found"
    assert data["status"] is False

@pytest.mark.asyncio
async def test_return_forbidden_patch_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_two = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    dto = UpdateSavedSearchDTO(
        name = None,
        query = dict({"name": "new name"}),
        description = None,
        is_public = None,
        last_executed_at = None,
        notifications_enabled = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.patch(
            f"{URL}/{saved_search_data.id}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 403
    assert data["body"] is None
    assert data["code"] == 403
    assert data["message"] == "You cannot to update this search"
    assert data["status"] is False

@pytest.mark.asyncio
async def test_patch_saved_search_successfully():
    user_data = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    dto = dict(UpdateSavedSearchDTO(
        name = "any name",
        query = dict({"name": "any name"}),
        description = None,
        is_public = True,
        last_executed_at = None,
        notifications_enabled = False,
    ))

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.patch(
            f"{URL}/{saved_search_data.id}",
            json=dto,
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200
    assert data["body"] is not None
    assert data["body"]["id"] == saved_search_data.id
    assert data["body"]["user_id"] == saved_search_data.user_id
    assert data["body"]["name"] == dto["name"]
    assert data["body"]["query"] == dto["query"]
    assert data["body"]["description"] == dto["description"]
    assert data["body"]["is_public"] == dto["is_public"]
    assert data["body"]["notifications_enabled"] == dto["notifications_enabled"]
    assert data["message"] == "Search updated with successfully"
    assert data["code"] == 200

@pytest.mark.asyncio
async def test_return_forbbirn_patch_toggle_public_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_two = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{saved_search_data.id}/toggle/status/is-public",
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 403

    assert data['body'] is None
    assert data['message'] == "You cannot to change status this search"
    assert data['code'] == 403

@pytest.mark.asyncio
async def test_patch_toggle_public_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{saved_search_data.id}/toggle/status/is-public",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is not None
    assert data['body']['id'] == saved_search_data.id
    assert data['body']['user_id'] == saved_search_data.user_id
    assert data['body']['is_public'] == (not saved_search_data.is_public)
    assert data['message'] == "Search changed status public with successfully"
    assert data['code'] == 200

@pytest.mark.asyncio
async def test_return_bad_request_patch_toggle_public_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}/toggle/status/is-public",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_patch_toggle_public_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{999999999}/toggle/status/is-public",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['code'] == 404
    assert data['message'] == "Search not found"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_forbbirn_patch_toggle_noti_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_two = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{saved_search_data.id}/toggle/status/notifications-enabled",
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 403

    assert data['body'] is None
    assert data['message'] == "You cannot to change status this search"
    assert data['code'] == 403

@pytest.mark.asyncio
async def test_patch_toggle_noti_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{saved_search_data.id}/toggle/status/notifications-enabled",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is not None
    assert data['body']['id'] == saved_search_data.id
    assert data['body']['user_id'] == saved_search_data.user_id
    assert data['body']['notifications_enabled'] == (not saved_search_data.notifications_enabled)
    assert data['message'] == "Search changed status notifications enabled with successfully"
    assert data['code'] == 200

@pytest.mark.asyncio
async def test_return_bad_request_patch_toggle_noti_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{0}/toggle/status/notifications-enabled",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_patch_toggle_noti_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.patch(
            f"{URL}/{999999999}/toggle/status/notifications-enabled",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['code'] == 404
    assert data['message'] == "Search not found"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_forbbirn_delete_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    user_data_two = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{saved_search_data.id}",headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 403

    assert data['body'] is None
    assert data['message'] == "You cannot to delete this search"
    assert data['code'] == 403

@pytest.mark.asyncio
async def test_delete_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{saved_search_data.id}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body'] is None
    assert data['message'] == "Search deleted with successfully"
    assert data['code'] == 200

@pytest.mark.asyncio
async def test_return_bad_request_delete_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{0}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_delete_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.delete(
            f"{URL}/{999999999}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['code'] == 404
    assert data['message'] == "Search not found"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_bad_request_get_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{0}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 400

    assert data['body'] is None
    assert data['code'] == 400
    assert data['message'] == "Id is required"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_return_not_found_get_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{999999999}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 404

    assert data['body'] is None
    assert data['code'] == 404
    assert data['message'] == "Search not found"
    assert data['status'] == False

@pytest.mark.asyncio
async def test_get_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()
    saved_search_data = await create_saved_search(user_data)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.get(
            f"{URL}/{saved_search_data.id}",headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 200

    assert data['body']['id'] == saved_search_data.id
    assert data['body']['user_id'] == saved_search_data.user_id
    assert data['body']['name'] == saved_search_data.name

@pytest.mark.asyncio
async def test_create_saved_search():
    user_data = await create_and_login_user_with_role_super_adm()

    dto = CreateSavedSearchDTO(
        name = "any query",
        query = dict({"name__ilike": "any"}),
        description = None,
        is_public = True,
        last_executed_at = None,
        notifications_enabled = False
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}", json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['user_id'] == user_data.out.id
    assert data['body']['name'] == dto.name