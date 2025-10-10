from fastapi_filter.contrib.sqlalchemy import Filter

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum


class ReactionCommentPostEnterpriseFilter(Filter):
    user_id: int | None
    comment_enterprise_id: int | None
    reaction_type: ReactionTypeEnum | None

    class Constants(Filter.Constants):
        model = ReactionCommentPostEnterpriseEntity