from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel


class EnterpriseMetricOUT(ORJSONModel):
    enterprise_id: int
    follower_count: int
    vacancies_count: int
    post_count: int
    comment_post: int
    followed_count: int
    view_count: int
    review_count: int
    employments_count: int
    last_activity_at: datetime | None
    created_at: datetime
    updated_at: datetime