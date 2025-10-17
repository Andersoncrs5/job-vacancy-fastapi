from datetime import datetime

from app.configs.db.enums import NotificationTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel


class NotificationOUT(ORJSONModel):
    id: int
    user_id: int
    title: str
    content: str
    link: str | None
    is_view: bool
    type: NotificationTypeEnum
    entity_id: int | None
    created_at: datetime
    updated_at: datetime