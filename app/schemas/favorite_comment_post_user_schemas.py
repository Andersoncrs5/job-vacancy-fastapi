import uuid
from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.comment_post_enterprise_schemas import CommentPostEnterpriseOUT
from app.schemas.user_schemas import UserOUT


class FavoriteCommentPostEnterpriseOUT(ORJSONModel):
    id: uuid.UUID
    user_id: int
    comment_enterprise_id: int
    created_at: datetime
    user: UserOUT
    comment: CommentPostEnterpriseOUT

class FavoriteCommentPostEnterpriseSimpleOUT(ORJSONModel):
    id: uuid.UUID
    user_id: int
    comment_enterprise_id: int
    created_at: datetime