from datetime import datetime
from uuid import UUID

from app.configs.orjson.orjson_config import ORJSONModel


class EventBase(ORJSONModel):
    event_id: UUID
    created_at: datetime
    source_service: str
    data: dict
    metadata: dict