import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import UserEntity
from app.schemas.user_schemas import CreateUserDTO
import random
from typing import Any, Dict, Final

@pytest.mark.asyncio
def test_register_user(test_client: TestClient, async_session: AsyncSession):
    num: Final[int] = random.randint(100000,1000000000)

    dto: Final = CreateUserDTO(
        name = f"user {num}",
        email = f"user{num}@gmail.com",
        password = f"{num}"
    )

    response: Final = test_client.post(
        url="/api/v1/auth/register",
        json=dict(dto)
    )

    assert response.status_code == 201