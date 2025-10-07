from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.enterprise_schemas import EnterpriseOUT
from app.schemas.user_schemas import UserOUT

class FollowEnterpriseOUT(ORJSONModel):
    user_id: int
    enterprise_id: int
    created_at: datetime
    follower: UserOUT
    followed_enterprise: EnterpriseOUT