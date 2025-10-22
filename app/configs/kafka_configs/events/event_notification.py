from app.configs.db.enums import NotificationTypeEnum
from app.configs.kafka_configs.events.base import EventBase


class EventNotification(EventBase):
    event_type: NotificationTypeEnum
    actor_id: int | None
    entity_id: int