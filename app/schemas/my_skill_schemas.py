from app.configs.orjson.orjson_config import ORJSONModel
from uuid import UUID
from datetime import datetime, date
from app.configs.db.enums import ProficiencyEnum

class MySkillOUT(ORJSONModel):
    user_id: int
    skill_id: UUID
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date

class UpdateMySkillDTO(ORJSONModel):
    skill_id: UUID | None
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date

class CreateMySkillDTO(ORJSONModel):
    skill_id: UUID | None
    proficiency: ProficiencyEnum | None
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date | None

