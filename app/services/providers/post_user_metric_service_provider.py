from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import PostUserMetricEntity
from app.configs.kafka.kafka import SUM_RED_METRIC_TOPIC
from app.repositories.providers.post_user_metric_repository_provider import PostUserMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.post_user_metric_service_base import PostUserMetricServiceBase

import uuid

from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import ColumnsPostUserMetricEnum, SumRedEnum


class PostUserMetricServiceProvider(PostUserMetricServiceBase):
    def __init__(self, repository: PostUserMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        return await self.repository.get_by_id(post_id)

    async def delete(self, metric: PostUserMetricEntity) -> None:
        await self.repository.delete(metric)

    async def create(self, post_id) -> PostUserMetricEntity:
        metric = PostUserMetricEntity(post_id=post_id)

        return await self.repository.add(metric)

    async def update_metric(self, post_id: int, column: ColumnsPostUserMetricEnum, action: SumRedEnum):
        if column not in ColumnsPostUserMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=post_id,
            column=column,
            action=action,
            entity=EntityEnum.POST_USER_METRIC,
            source="post-user-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4()),
            metadata=dict({})
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)