from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas
from app.schemas.roles_schemas import RoleOUT
from app.schemas.user_schemas import UserOUT


class UserRolesOUT(BaseSchemas):
    id: int
    user_id: int
    role_id: int
    user: UserOUT
    role: RoleOUT
