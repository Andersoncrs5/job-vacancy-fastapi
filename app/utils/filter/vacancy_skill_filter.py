from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import VacancySkillEntity
from app.configs.db.enums import ProficiencyEnum


class VacancySkillFilter(Filter):
    vacancy_id: Optional[int] = Field(None)
    skill_id: Optional[int] = Field(None)
    is_required: Optional[bool] = Field(None)
    proficiency: Optional[ProficiencyEnum] = Field(None)
    years_experience__gte: Optional[int] = Field(None)
    years_experience__lte: Optional[int] = Field(None)
    priority_level__gte: Optional[int] = Field(None)
    priority_level__lte: Optional[int] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = VacancySkillEntity