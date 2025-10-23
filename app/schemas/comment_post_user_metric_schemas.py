from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class CommentPostUserMetricOUT(BaseSchemas):
    comment_id: int
    replies_count: int
    edited_count: int
    views_count: int
    shares_count: int
    reactions_like_count: int
    reactions_dislike_count: int
    favorites_count: int