from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime, date
from app.configs.db.enums import ProficiencyEnum

class MySkillOUT(ORJSONModel):
    user_id: int
    skill_id: int
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date | str
    created_at: datetime | str
    updated_at: datetime | str

class UpdateMySkillDTO(ORJSONModel):
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date | None

class CreateMySkillDTO(ORJSONModel):
    skill_id: int
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

