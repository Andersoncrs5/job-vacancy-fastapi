from fastapi.testclient import TestClient
from typing import Final
from tests.integration.helper import create_and_login_user, create_skill
from main import app
from httpx import ASGITransport, AsyncClient
from app.schemas.my_skill_schemas import *
import pytest
import random
from uuid import UUID, uuid4
from app.configs.db.enums import ProficiencyEnum

client: Final[TestClient] = TestClient(app)
URL: Final[str] = '/api/v1/my-skill'

@pytest.mark.asyncio
async def test_create_my_skill():
    user_data = await create_and_login_user()
    skill = await create_skill(user_data)

    dto = CreateMySkillDTO(
        skill_id = skill.id,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201    

    assert data['body']['skill_id'] == dto.skill_id
    assert data['body']['proficiency'] == dto.proficiency
    assert data['body']['certificate_url'] == dto.certificate_url
    assert data['body']['datails'] == dto.datails
    assert data['body']['years_of_experience'] == dto.years_of_experience