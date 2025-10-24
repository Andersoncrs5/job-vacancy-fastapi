from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import AreaEntity
from app.utils.filter.user_filter import UserFilter


class AreaFilter(Filter):
    name__ilike: Optional[str] = Field(None, description="Search by name (case-insensitive).")
    description__ilike: Optional[str] = Field(None, description="Search by description (case-insensitive).")
    is_active: Optional[bool] = Field(None, description="Search by is active")
    user_id: Optional[int] = Field(None, description="Search by user ID")
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = AreaEntity