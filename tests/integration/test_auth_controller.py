from fastapi.testclient import TestClient
from typing import Final
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from main import app
import random

client: Final[TestClient] = TestClient(app)

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

def test_login_user():
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

    dto_login = LoginDTO(
        email = dto.email,
        password = dto.password,
    )

    response = client.post(
        "/api/v1/auth/login",
        json=dict(dto_login)
    )

    assert response.status_code == 200