from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime
from app.configs.db.enums import ProficiencyEnum
from app.schemas.skill_schemas import SkillOUT

class VacancySkillOUT(ORJSONModel):
    is_required: bool
    proficiency: ProficiencyEnum | None
    years_experience: int | None
    priority_level: int | None
    notes: str | None
    skill: SkillOUT
    