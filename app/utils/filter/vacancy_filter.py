from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import VacancyEntity
from app.configs.db.enums import EmploymentTypeEnum, ExperienceLevelEnum, EducationLevelEnum, WorkplaceTypeEnum, \
    VacancyStatusEnum


class VacancyFilter(Filter):
    enterprise_id: Optional[int] = Field(None)
    area_id: Optional[int] = Field(None)
    title__ilike: Optional[str] = Field(None)
    description__ilike: Optional[str] = Field(None)
    employment_type: Optional[EmploymentTypeEnum] = Field(None)
    experience_level: Optional[ExperienceLevelEnum] = Field(None)
    education_level: Optional[EducationLevelEnum] = Field(None)
    workplace_type: Optional[WorkplaceTypeEnum] = Field(None)
    seniority__gte: Optional[int] = Field(None)
    seniority__lte: Optional[int] = Field(None)
    salary_min__gte: Optional[float] = Field(None)
    salary_min__lte: Optional[float] = Field(None)
    salary_max__gte: Optional[float] = Field(None)
    salary_max__lte: Optional[float] = Field(None)
    currency__ilike: Optional[str] = Field(None)
    requirements__ilike: Optional[str] = Field(None)
    status: Optional[VacancyStatusEnum] = Field(None)
    openings__gte: Optional[int] = Field(None)
    openings__lte: Optional[int] = Field(None)
    application_deadline__gte: Optional[datetime] = Field(None)
    application_deadline__lte: Optional[datetime] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = VacancyEntity