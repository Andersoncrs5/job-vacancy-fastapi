from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime, date
from app.configs.db.database import EmployeeEnterpriseEntity
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum


class EmployeeEnterpriseFilter(Filter):
    user_id: Optional[int] = Field(None)
    enterprise_id: Optional[int] = Field(None)
    position__ilike: Optional[str] = Field(None)
    salary_range__ilike: Optional[str] = Field(None)
    employment_type: Optional[EmploymentTypeEnum] = Field(None)
    employment_status: Optional[EmploymentStatusEnum] = Field(None)
    start_date__gte: Optional[date] = Field(None)
    start_date__lte: Optional[date] = Field(None)
    end_date__gte: Optional[date] = Field(None)
    end_date__lte: Optional[date] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = EmployeeEnterpriseEntity