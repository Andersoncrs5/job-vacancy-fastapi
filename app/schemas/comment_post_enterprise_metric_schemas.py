from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel


class CommentPostEnterpriseMetricOUT(ORJSONModel):
    comment_id: int
    replies_count: int
    edited_count: int
    views_count: int
    shares_count: int
    reactions_like_count: int
    reactions_dislike_count: int
    favorites_count: int
    created_at: datetime
    updated_at: datetime