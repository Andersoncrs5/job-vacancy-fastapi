from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.user_schemas import UserOUT


class FollowOUT(ORJSONModel):
    follower_id: int
    followed_id: int
    created_at: datetime
    follower: UserOUT
    followed: UserOUT