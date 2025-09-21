import random
from httpx import ASGITransport, AsyncClient
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from main import app
from typing import Final
from pydantic import BaseModel
from app.utils.res.tokens import Tokens
from app.schemas.category_schemas import *

class UserTestData(BaseModel):
    dto: CreateUserDTO
    tokens: Tokens

async def create_category(user_data: UserTestData):
    num = random.randint(10000,100000000000)

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    data = response.json()

    assert data['code'] == 201
    assert data['message'] == 'Category created with successfully'
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None

    assert data['body']['id'] is not None
    assert data['body']['name'] == dto.name
    assert data['body']['slug'] == dto.slug
    assert data['body']['description'] == dto.description
    assert data['body']['order'] == dto.order
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['is_active'] == True
    assert data['body']['user_id'] is not None
    assert data['body']['created_at'] is not None

    return CategoryOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        slug = data['body']['slug'],
        description = data['body']['description'],
        is_active = data['body']['is_active'],
        order = data['body']['order'],
        post_count = data['body']['post_count'],
        job_count = data['body']['job_count'],
        icon_url = data['body']['icon_url'],
        user_id = data['body']['user_id'],
        parent_id = data['body']['parent_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_and_login_user() -> UserTestData:
    num = random.randint(1000000, 10000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dto.model_dump())
    assert response.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_dto = LoginDTO(email=dto.email, password=dto.password)
        response = await ac.post("/api/v1/auth/login", json=login_dto.model_dump())
    assert response.status_code == 200

    data = response.json()["body"]

    tokens = Tokens(
        token=data["token"],
        refresh_token=data["refresh_token"],
        exp_token=data.get("exp_token"),
        exp_refresh_token=data.get("exp_refresh_token"),
    )

    return UserTestData(dto=dto, tokens=tokens)
