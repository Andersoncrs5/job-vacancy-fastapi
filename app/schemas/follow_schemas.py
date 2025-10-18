from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.user_schemas import UserOUT


class FollowOUT(ORJSONModel):
    follower_id: int
    followed_id: int
    receive_post: bool
    receive_comment: bool
    created_at: datetime
    follower: UserOUT
    followed: UserOUT

class UpdateFollowDTO(ORJSONModel):
    receive_post: bool | None
    receive_comment: bool | None