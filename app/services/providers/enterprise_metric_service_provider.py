from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import EnterpriseMetricEntity
from app.configs.kafka_configs.kafka_admin import SUM_RED_METRIC_TOPIC
from app.repositories.providers.enterprise_metric_repository_provider import EnterpriseMetricRepositoryProvider
from app.schemas.event_message_schemas import EventMessageMetric, EntityEnum
from app.services.base.enterprise_metric_service_base import EnterpriseMetricServiceBase
from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import ColumnEnterpriseMetricEnum, SumRedEnum

import uuid

class EnterpriseMetricServiceProvider(EnterpriseMetricServiceBase):
    def __init__(self, repository: EnterpriseMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        return await self.repository.get_by_id(enterprise_id)

    async def exists_by_id(self, enterprise_id: int) -> bool:
        return await self.repository.exists_by_id(enterprise_id)

    async def delete(self, metric: EnterpriseMetricEntity) -> None:
        await self.repository.delete(metric)

    async def create(self, enterprise_id: int) -> None:
        metric = EnterpriseMetricEntity(
            enterprise_id = enterprise_id
        )

        await self.repository.add(metric)

    async def update_metric(self, enterprise_id, column: ColumnEnterpriseMetricEnum,
                            action: SumRedEnum):

        if column not in ColumnEnterpriseMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=enterprise_id,
            column=column,
            action=action,
            entity=EntityEnum.ENTERPRISE_METRIC,
            source="enterprise-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4()),
            metadata=dict({})
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)