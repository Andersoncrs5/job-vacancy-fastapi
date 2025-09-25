from app.configs.orjson.orjson_config import ORJSONModel
from uuid import UUID
from datetime import datetime, date
from app.configs.db.enums import ProficiencyEnum
from app.configs.db.database import MySkillEntity

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
    last_used_date: date | None

class CreateMySkillDTO(ORJSONModel):
    skill_id: UUID
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date

    def to_entity(self):
        from app.configs.db.database import MySkillEntity

        return MySkillEntity(
            skill_id = self.skill_id,
            proficiency = self.proficiency,
            certificate_url = self.certificate_url,
            datails = self.datails,
            years_of_experience = self.years_of_experience,
            last_used_date = self.last_used_date,
        )

