from datetime import datetime

from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas
from app.schemas.post_user_schemas import PostUserOUT
from app.schemas.user_schemas import UserOUT


class CommentPostUserOUT(BaseSchemas):
    id: int
    content: str
    user_id: int
    post_user_id: int
    parent_comment_id: int | None
    is_edited: bool
    user: UserOUT | None
    post: PostUserOUT | None

class CreateCommentPostUserDTO(ORJSONModel):
    content: str = Field(..., min_length=1, max_length=2000, description="The comment content (max 2000 characters).")
    post_user_id: int = Field(..., ge=1, description="The ID of the user post being commented on.")
    parent_comment_id: int | None = Field(None, ge=1, description="The ID of the parent comment, if this is a reply.")

    def to_entity(self):
        from app.configs.db.database import CommentPostUserEntity
        return CommentPostUserEntity(**self.model_dump(exclude_none=True))

class UpdateCommentPostUserDTO(ORJSONModel):
    content: str | None = Field(None, min_length=1, max_length=2000, description="The updated comment content (max 2000 characters).")