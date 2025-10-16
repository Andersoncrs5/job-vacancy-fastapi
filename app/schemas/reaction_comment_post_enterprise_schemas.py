
from datetime import datetime
from uuid import UUID

from pydantic import Field

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
    comment_enterprise_id: int = Field(..., ge=1, description="The ID of the comment enterprise this post belongs to.")
    reaction_type: ReactionTypeEnum = Field(..., description="The type of reaction being registered.")
