from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class RoleOUT(BaseSchemas):
    id: int
    title: str
    slug: str
    is_active: bool
    is_immutable: bool