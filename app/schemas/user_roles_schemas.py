from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.roles_schemas import RoleOUT
from app.schemas.user_schemas import UserOUT


class UserRolesOUT(ORJSONModel):
    id: int
    user_id: int
    role_id: int
    user: UserOUT
    role: RoleOUT
    created_at: datetime | str
    updated_at: datetime | str
