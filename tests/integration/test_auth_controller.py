from fastapi.testclient import TestClient
from typing import Final
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from main import app
import random
from httpx import ASGITransport, AsyncClient
import pytest

client: Final[TestClient] = TestClient(app)

@pytest.mark.asyncio
def test_register_user():
    num = random.randint(1000000,10000000000000)
    dto = CreateUserDTO(
        name = f"user {num}",
        email = f"user{num}@example.com",
        password = str(num),
        bio = None,
        avatar_url = None,
    )

    response = client.post(
        "/api/v1/auth/register",
        json=dict(dto)
    )

    assert response.status_code == 201

@pytest.mark.anyio
async def test_register_and_login_user():
    num = random.randint(1000000, 10000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dto.dict())
        assert response.status_code == 201


    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        dto_login = LoginDTO(email=dto.email, password=dto.password)
        response = await ac.post("/api/v1/auth/login", json=dto_login.dict())
        assert response.status_code == 200
