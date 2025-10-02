from app.configs.orjson.orjson_config import ORJSONModel
from app.configs.db.enums import ProficiencyEnum
from app.schemas.skill_schemas import SkillOUT

class VacancySkillOUT(ORJSONModel):
    is_required: bool
    proficiency: ProficiencyEnum | None
    years_experience: int | None
    priority_level: int | None
    notes: str | None
    skill: SkillOUT
    
class CreateVacancySkillDTO(ORJSONModel):
    vacancy_id: int
    skill_id: int
    is_required: bool
    proficiency: ProficiencyEnum | None
    years_experience: int | None
    priority_level: int | None
    notes: str | None

    def to_entity(self):
        from app.configs.db.database import VacancySkillEntity

        return VacancySkillEntity(
            vacancy_id = self.vacancy_id,
            skill_id = self.skill_id,
            is_required = self.is_required,
            proficiency = self.proficiency,
            years_experience = self.years_experience,
            priority_level = self.priority_level,
            notes = self.notes,
        )


class UpdateVacancySkillDTO(ORJSONModel):
    is_required: bool | None
    proficiency: ProficiencyEnum | None
    years_experience: int | None
    priority_level: int | None
    notes: str | None

