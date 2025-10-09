import uuid
from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.comment_post_user_schemas import CommentPostUserOUT
from app.schemas.user_schemas import UserOUT


class FavoriteCommentPostUserOUT(ORJSONModel):
    id: uuid.UUID
    user_id: int
    comment_user_id: int
    created_at: datetime
    user: UserOUT
    comment: CommentPostUserOUT

class FavoriteCommentPostUserSimpleOUT(ORJSONModel):
    id: uuid.UUID
    user_id: int
    comment_user_id: int
    created_at: datetime