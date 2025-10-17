from datetime import datetime
from uuid import UUID

from app.configs.orjson.orjson_config import ORJSONModel


class EventNotification(ORJSONModel):
    event_id: UUID
    user_id: int
    created_at: datetime
    source_service: str
    data: dict
    metadata: dict