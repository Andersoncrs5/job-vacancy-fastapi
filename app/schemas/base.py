from datetime import datetime

from app.configs.db.enums import NotificationTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel

class BaseSchemas(ORJSONModel):
    created_at: datetime
    updated_at: datetime

class NotificationBaseOUT(BaseSchemas):
    id: int
    title: str
    content: str
    link: str | None = None
    is_view: bool
    type: NotificationTypeEnum
    entity_id: int  | None = None