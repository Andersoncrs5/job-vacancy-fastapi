from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum


class ReactionCommentPostEnterpriseFilter(Filter):
    user_id: Optional[int] = Field(None)
    comment_enterprise_id: Optional[int] = Field(None)
    reaction_type: Optional[ReactionTypeEnum] = Field(None)

    class Constants(Filter.Constants):
        model = ReactionCommentPostEnterpriseEntity