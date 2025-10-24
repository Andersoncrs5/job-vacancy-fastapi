from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import ReviewEnterprise
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum


class ReviewEnterpriseFilter(Filter):
    title__ilike: Optional[str] = Field(None, description="Search by name (case-insensitive).")
    description__ilike: Optional[str] = Field(None, description="Search by name (case-insensitive).")
    rating__gte: Optional[int] = Field(None)
    rating__lte: Optional[int] = Field(None)
    would_recommend: Optional[bool] = Field(None)
    position__ilike: Optional[str] = Field(None)
    salary_range__ilike: Optional[str] = Field(None)
    employment_type: Optional[EmploymentTypeEnum] = Field(None)
    employment_status: Optional[EmploymentStatusEnum] = Field(None)
    helpful_votes__gte: Optional[int] = Field(None)
    helpful_votes__lte: Optional[int] = Field(None)
    unhelpful_votes__gte: Optional[int] = Field(None)
    unhelpful_votes__lte: Optional[int] = Field(None)
    user_id: Optional[int] = Field(None)
    enterprise_id: Optional[int] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = ReviewEnterprise