import uuid
from datetime import datetime

from app.configs.db.enums import ReactionTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.comment_post_user_schemas import CommentPostUserOUT
from app.schemas.user_schemas import UserOUT


class ReactionCommentPostUserOUT(ORJSONModel):
    id: uuid.UUID
    user_id: int
    comment_user_id: int
    reaction_type: ReactionTypeEnum
    created_at: datetime
    user: UserOUT
    comment: CommentPostUserOUT

class CreateReactionCommentPostUserDTO(ORJSONModel):
    comment_user_id: int
    reaction_type: ReactionTypeEnum