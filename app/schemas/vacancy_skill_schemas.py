from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from app.configs.db.enums import ProficiencyEnum
from app.schemas.skill_schemas import SkillOUT
from app.schemas.vacancy_schemas import VacancyOUT

class VacancySkillOUT(ORJSONModel):
    is_required: bool
    proficiency: ProficiencyEnum | None
    years_experience: int | None
    priority_level: int | None
    notes: str | None
    skill: SkillOUT
    vacancy: VacancyOUT
    
class CreateVacancySkillDTO(ORJSONModel):
    vacancy_id: int = Field(..., ge=1, description="The ID of the vacancy the skill is being added to.")
    skill_id: int = Field(..., ge=1, description="The ID of the skill being added.")
    is_required: bool = Field(True, description="Whether this skill is mandatory for the vacancy.")
    proficiency: ProficiencyEnum | None = Field(None, description="The minimum proficiency level required for the skill.")
    years_experience: int | None = Field(None, ge=0, description="Minimum years of experience required (must be non-negative).")
    priority_level: int | None = Field(None, ge=1, le=10, description="Priority level of the skill (1=low, 10=high).")
    notes: str | None = Field(None, max_length=500, description="Additional notes regarding the skill requirement (max 500 characters).")

    def to_entity(self):
        from app.configs.db.database import VacancySkillEntity

        return VacancySkillEntity(**self.model_dump(exclude_none=True))

class UpdateVacancySkillDTO(ORJSONModel):
    is_required: bool | None = Field(None, description="Whether this skill is mandatory for the vacancy.")
    proficiency: ProficiencyEnum | None = Field(None,
                                                description="The minimum proficiency level required for the skill.")
    years_experience: int | None = Field(None, ge=0,
                                         description="Minimum years of experience required (must be non-negative).")
    priority_level: int | None = Field(None, ge=1, le=10, description="Priority level of the skill (1=low, 10=high).")
    notes: str | None = Field(None, max_length=500,
                              description="Additional notes regarding the skill requirement (max 500 characters).")
