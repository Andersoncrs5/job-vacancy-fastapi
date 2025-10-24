from datetime import datetime
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum


class ReactionCommentPostEnterpriseFilter(Filter):
    user_id: Optional[int] = Field(None)
    comment_enterprise_id: Optional[int] = Field(None)
    reaction_type: Optional[ReactionTypeEnum] = Field(None)
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = ReactionCommentPostEnterpriseEntity