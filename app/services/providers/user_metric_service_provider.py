from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import UserMetricEntity
from app.configs.db.kafka import SUM_RED_METRIC_TOPIC
from app.repositories.providers.user_metric_repository_provider import UserMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.user_metric_service_base import UserMetricServiceBase
from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import SumRedEnum, ColumnUserMetricEnum

import uuid

class UserMetricServiceProvider(UserMetricServiceBase):
    def __init__(self, repository: UserMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def get_by_id(self, user_id: int) -> UserMetricEntity | None:
        return await self.repository.get_by_id(user_id)

    async def create(self, user_id: int) -> UserMetricEntity:
        metric = UserMetricEntity(user_id = user_id)

        return await self.repository.add(metric)

    async def delete(self, metric: UserMetricEntity):
        await self.repository.delete(metric)

    async def update_metric(self, metric: UserMetricEntity, column: ColumnUserMetricEnum, action: SumRedEnum):
        if column not in ColumnUserMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=metric.user_id,
            column=column,
            action=action,
            entity=EntityEnum.USER_METRIC,
            source = "user-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4())
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)

    async def update_metric_v2(self, user_id, column: ColumnUserMetricEnum, action: SumRedEnum):
            if column not in ColumnUserMetricEnum.__members__.values():
                raise ValueError(f"Column invalid: {column}")

            event = EventMessageMetric(
                metric_id=user_id,
                column=column,
                action=action,
                entity=EntityEnum.USER_METRIC,
                source="user-metric-service",
                created_at=datetime.now(UTC),
                event_id=str(uuid.uuid4())
            )

            await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)

