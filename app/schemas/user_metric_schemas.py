from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel


class UserMetricOUT(ORJSONModel):
    user_id: int
    post_count: int
    favorite_post_count: int
    comment_count: int
    favorite_comment_count: int
    follower_count: int
    followed_count: int
    share_count: int
    connection_count: int
    blocked_count: int
    reaction_comment_given_count: int
    reaction_comment_received_count: int
    enterprise_follow_count: int
    enterprise_follower_count: int
    profile_view_count: int
    vacancy_application_count: int
    last_login_at: datetime | None
    last_post_at: datetime | None
    last_comment_at: datetime | None
    created_at: datetime
    updated_at: datetime