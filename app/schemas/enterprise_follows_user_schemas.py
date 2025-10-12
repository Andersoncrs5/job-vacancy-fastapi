from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.enterprise_schemas import EnterpriseOUT
from app.schemas.user_schemas import UserOUT


class EnterpriseFollowsUserOUT(ORJSONModel):
    id: int
    enterprise_id: int
    user_id: int
    created_at: datetime
    follower_enterprise: EnterpriseOUT
    followed_user: UserOUT