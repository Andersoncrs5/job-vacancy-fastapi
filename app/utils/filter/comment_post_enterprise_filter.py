from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import CommentPostEnterpriseEntity

class CommentPostEnterpriseFilter(Filter):
    content__ilike: Optional[str] = Field(None,description="Search by content (case-insensitive, LIKE).")
    user_id: Optional[int] = Field(None, description="Search by user ID")
    post_enterprise_id: Optional[int] = Field(None, description="Search by user ID")
    parent_comment_id: Optional[int] = Field(None, description="Search by user ID")
    is_edited: Optional[bool] = Field(None, description="Search by edited")
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = CommentPostEnterpriseEntity