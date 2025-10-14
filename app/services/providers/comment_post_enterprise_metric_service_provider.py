from datetime import datetime, UTC

import uuid
from aiokafka import AIOKafkaProducer

from app.configs.db.database import CommentPostEnterpriseMetricEntity
from app.configs.kafka_configs.kafka_admin import SUM_RED_METRIC_TOPIC
from app.repositories.providers.comment_post_enterprise_metric_repository_provider import \
    CommentPostEnterpriseMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.comment_post_enterprise_metric_service_base import CommentPostEnterpriseMetricServiceBase
from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import ColumnsCommentPostEnterpriseMetricEnum, SumRedEnum


class CommentPostEnterpriseMetricServiceProvider(CommentPostEnterpriseMetricServiceBase):
    def __init__(self, repository: CommentPostEnterpriseMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def create(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        metric = CommentPostEnterpriseMetricEntity(comment_id = comment_id)

        return await self.repository.add(metric)

    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        return await self.repository.get_by_id(comment_id)

    async def delete(self, metric: CommentPostEnterpriseMetricEntity) -> None:
        await self.repository.delete(metric)

    async def update_metric(self, comment_id: int, column: ColumnsCommentPostEnterpriseMetricEnum, action: SumRedEnum):
        if column not in ColumnsCommentPostEnterpriseMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=comment_id,
            column=column,
            action=action,
            entity=EntityEnum.COMMENT_POST_ENTERPRISE_METRIC,
            source="comment-post-user-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4()),
            metadata=dict({})
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)