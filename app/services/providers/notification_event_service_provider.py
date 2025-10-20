from datetime import datetime
from uuid import uuid4

from aiokafka import AIOKafkaProducer

from app.configs.db.enums import NotificationTypeEnum
from app.configs.kafka_configs.events.event_notification import EventNotification
from app.configs.kafka_configs.kafka_admin import NOTIFICATION_TOPIC
from app.services.base.notification_event_service_base import NotificationEventServiceBase
from app.services.kafka_service import send_message_to_kafka


class NotificationEventServiceProvider(NotificationEventServiceBase):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def notify_user_about(self, entity_id: int, actor_id: int | None, _type: NotificationTypeEnum, data: dict):
        event = EventNotification(
            event_id = uuid4(),
            actor_id = actor_id,
            event_type = _type,
            entity_id = entity_id,
            created_at = datetime.now(),
            source_service = "NotificationEventServiceProvider | notify_user_about",
            data = data,
            metadata = {}
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), NOTIFICATION_TOPIC)

    async def notify_event_to_kafka(self, entity_id: int, actor_id: int | None, _type: NotificationTypeEnum, data: dict):
        event = EventNotification(
            event_id=uuid4(),
            actor_id=actor_id,
            event_type=_type,
            entity_id=entity_id,
            created_at=datetime.now(),
            source_service="NotificationEventServiceProvider | notify_user_about",
            data=data,
            metadata={}
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), NOTIFICATION_TOPIC)