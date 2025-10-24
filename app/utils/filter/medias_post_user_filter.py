from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import MediaPostUserEntity
from app.configs.db.enums import MediaType


class MediaPostUserFilter(Filter):
    type: Optional[MediaType] = Field(None)
    order__gte: Optional[int] = Field(None)
    order__lte: Optional[int] = Field(None)
    size__gte: Optional[int] = Field(None)
    size__lte: Optional[int] = Field(None)
    caption__ilike: Optional[str] = Field(None)
    mime_type__ilike: Optional[str] = Field(None, description="Search by mime_type (case-insensitive).")
    post_id: Optional[int] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = MediaPostUserEntity