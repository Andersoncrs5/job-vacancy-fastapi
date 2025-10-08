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

class CreateCommentPostEnterpriseDTO(ORJSONModel):
    content: str
    post_enterprise_id: int
    parent_comment_id: int | None

    def to_entity(self):
        from app.configs.db.database import CommentPostEnterpriseEntity

        return CommentPostEnterpriseEntity(
            content=self.content,
            post_enterprise_id=self.post_enterprise_id,
            parent_comment_id=self.parent_comment_id,
        )

class UpdateCommentPostEnterpriseDTO(ORJSONModel):
    content: str | None