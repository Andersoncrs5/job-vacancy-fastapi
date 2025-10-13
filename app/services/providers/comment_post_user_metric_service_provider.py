from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import CommentPostUserMetricEntity
from app.configs.kafka.kafka import SUM_RED_METRIC_TOPIC
from app.repositories.providers.comment_post_user_metric_repository_provider import \
    CommentPostUserMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.comment_post_user_metric_service_base import CommentPostUserMetricServiceBase

import uuid

from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import SumRedEnum, ColumnsCommentPostUserMetricEnum


class CommentPostUserMetricServiceProvider(CommentPostUserMetricServiceBase):
    def __init__(self, repository: CommentPostUserMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def create(self, comment_id: int) -> CommentPostUserMetricEntity:
        metric = CommentPostUserMetricEntity(comment_id = comment_id)

        return await self.repository.add(metric)

    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        return await self.repository.get_by_id(comment_id)

    async def delete(self, metric: CommentPostUserMetricEntity) -> None:
        await self.repository.delete(metric)

    async def update_metric(self, comment_id: int, column: ColumnsCommentPostUserMetricEnum, action: SumRedEnum):
        if column not in ColumnsCommentPostUserMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=comment_id,
            column=column,
            action=action,
            entity=EntityEnum.COMMENT_POST_USER_METRIC,
            source="comment-post-user-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4()),
            metadata=dict({})
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)