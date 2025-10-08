from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.post_user_schemas import PostUserOUT
from app.schemas.user_schemas import UserOUT


class CommentPostUserOUT(ORJSONModel):
    id: int
    content: str
    user_id: int
    post_user_id: int
    parent_comment_id: int | None
    is_edited: bool
    created_at: datetime
    updated_at: datetime
    user: UserOUT
    post: PostUserOUT

class CreateCommentPostUserDTO(ORJSONModel):
    content: str
    post_user_id: int

class UpdateCommentPostUserDTO(ORJSONModel):
    content: str | None