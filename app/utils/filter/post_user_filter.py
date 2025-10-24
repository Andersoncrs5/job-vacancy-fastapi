from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import PostUserEntity

class PostUserFilter(Filter):
    title__ilike: Optional[str] = Field(None, description="Search by title (case-insensitive).")
    content__ilike: Optional[str] = Field(None)
    user_id: Optional[int] = Field(None)
    category_id: Optional[int] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = PostUserEntity