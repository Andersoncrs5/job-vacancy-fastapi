from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import EnterpriseEntity

class EnterpriseFilter(Filter):
    name__ilike: Optional[str] = Field(None, description="Search by name (case-insensitive).")
    description__ilike: Optional[str] = Field(None, description="Search by description (case-insensitive).")
    user_id: Optional[int] = Field(None)
    industry_id: Optional[int] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = EnterpriseEntity