from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import MySkillEntity
from app.configs.db.enums import ProficiencyEnum


class MySkillFilter(Filter):
    user_id: Optional[int] = Field(None)
    skill_id: Optional[int] = Field(None)
    proficiency: Optional[ProficiencyEnum] = Field(None)
    datails__ilike: Optional[str] = Field(None)
    years_of_experience__gte: Optional[int] = Field(None)
    years_of_experience__lte: Optional[int] = Field(None)
    last_used_date__gte: Optional[date] = Field(None, description="Filter by creation date, greater than or equal to.")
    last_used_date__lte: Optional[date] = Field(None, description="Filter by creation date, less than or equal to.")
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = MySkillEntity