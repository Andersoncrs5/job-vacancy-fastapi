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
    user: UserOUT | None
    post: PostUserOUT | None

class CreateCommentPostUserDTO(ORJSONModel):
    content: str
    post_user_id: int
    parent_comment_id: int | None

    def to_entity(self):
        from app.configs.db.database import CommentPostUserEntity

        return CommentPostUserEntity(
            content=self.content,
            post_user_id=self.post_user_id,
            parent_comment_id=self.parent_comment_id,
        )

class UpdateCommentPostUserDTO(ORJSONModel):
    content: str | None