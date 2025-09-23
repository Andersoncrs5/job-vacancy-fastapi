from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import MediaPostUserEntity

class MediaPostUserFilter(Filter):
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = MediaPostUserEntity