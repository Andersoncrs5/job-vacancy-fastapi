from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import PostEnterpriseMetricEntity
from app.configs.kafka_configs.kafka_admin import SUM_RED_METRIC_TOPIC
from app.repositories.providers.post_enterprise_metric_repository_provider import PostEnterpriseMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.post_enterprise_metric_service_base import PostEnterpriseMetricServiceBase
from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import ColumnsPostEnterpriseMetricEnum, SumRedEnum

import uuid

class PostEnterpriseMetricServiceProvider(PostEnterpriseMetricServiceBase):
    def __init__(self, repository: PostEnterpriseMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        return await self.repository.get_by_id(post_id)

    async def create(self, post_id: int) -> PostEnterpriseMetricEntity:
        metric = PostEnterpriseMetricEntity(post_id = post_id)
        return await self.repository.add(metric)

    async def delete(self, metric: PostEnterpriseMetricEntity) -> None:
        await self.repository.delete(metric)

    async def update_metric(self, post_id, column: ColumnsPostEnterpriseMetricEnum, action: SumRedEnum):
            if column not in ColumnsPostEnterpriseMetricEnum.__members__.values():
                raise ValueError(f"Column invalid: {column}")

            event = EventMessageMetric(
                metric_id=post_id,
                column=column,
                action=action,
                entity=EntityEnum.POST_ENTERPRISE_METRIC,
                source="post-enterprise-metric-service",
                created_at=datetime.now(UTC),
                event_id=str(uuid.uuid4()),
                metadata=dict({})
            )

            await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)