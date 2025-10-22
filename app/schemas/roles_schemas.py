from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel


class RoleOUT(ORJSONModel):
    id: int
    title: str
    slug: str
    is_active: bool
    is_immutable: bool
    created_at: datetime
    updated_at: datetime