from datetime import datetime
from uuid import UUID

from app.configs.db.enums import ReactionTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.comment_post_enterprise_schemas import CommentPostEnterpriseOUT
from app.schemas.user_schemas import UserOUT


class ReactionCommentPostEnterpriseOUT(ORJSONModel):
    id: UUID
    user_id: int
    comment_enterprise_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime
    user: UserOUT
    comment: CommentPostEnterpriseOUT

class CreateReactionCommentPostEnterpriseDTO(ORJSONModel):
    comment_enterprise_id: int
    reaction_type: ReactionTypeEnum
