from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.post_enterprise_schemas import PostEnterpriseOUT
from app.schemas.user_schemas import UserOUT


class CommentPostEnterpriseOUT(ORJSONModel):
    id: int
    content: str
    user_id: int
    post_enterprise_id: int
    parent_comment_id: int | None
    is_edited: bool
    created_at: datetime
    updated_at: datetime
    user: UserOUT
    post: PostEnterpriseOUT

class CreateCommentPostUserDTO(ORJSONModel):
    content: str
    post_enterprise_id: int
    parent_comment_id: int | None

class UpdateCommentPostUserDTO(ORJSONModel):
    content: str | None