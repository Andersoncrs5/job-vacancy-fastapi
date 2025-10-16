from datetime import datetime

from pydantic import Field

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

class CreateCommentPostEnterpriseDTO(ORJSONModel):
    content: str = Field(..., min_length=1, max_length=800, description="The comment content (max 800 characters).")
    post_enterprise_id: int = Field(..., ge=1, description="The ID of the enterprise post being commented on.")
    parent_comment_id: int | None = Field(None, ge=1, description="The ID of the parent comment, if this is a reply.")

    def to_entity(self):
        from app.configs.db.database import CommentPostEnterpriseEntity
        return CommentPostEnterpriseEntity(**self.model_dump(exclude_none=True))

class UpdateCommentPostEnterpriseDTO(ORJSONModel):
    content: str | None = Field(None, min_length=1, max_length=800, description="The updated comment content (max 800 characters).")