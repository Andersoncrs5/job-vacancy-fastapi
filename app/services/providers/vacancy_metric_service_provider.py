from datetime import datetime, UTC

from aiokafka import AIOKafkaProducer

from app.configs.db.database import VacancyMetricEntity
from app.configs.db.kafka import SUM_RED_METRIC_TOPIC
from app.repositories.providers.vacancy_metric_repository_provider import VacancyMetricRepositoryProvider
from app.schemas.event_message_schemas import EntityEnum, EventMessageMetric
from app.services.base.vacancy_metric_service_base import VacancyMetricServiceBase
from app.services.kafka_service import send_message_to_kafka
from app.utils.enums.sum_red import ColumnsVacancyMetricEnum, SumRedEnum

import uuid

class VacancyMetricServiceProvider(VacancyMetricServiceBase):
    def __init__(self, repository: VacancyMetricRepositoryProvider, producer: AIOKafkaProducer):
        self.repository = repository
        self.producer = producer

    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        return await self.repository.get_by_id(vacancy_id)

    async def delete(self, metric: VacancyMetricEntity):
        await self.repository.delete(metric)

    async def create(self, vacancy_id: int) -> VacancyMetricEntity:
        metric = VacancyMetricEntity(vacancy_id=vacancy_id)

        return await self.repository.add(metric)

    async def update_metric(self, vacancy_id: int, column: ColumnsVacancyMetricEnum, action: SumRedEnum):
        if column not in ColumnsVacancyMetricEnum.__members__.values():
            raise ValueError(f"Column invalid: {column}")

        event = EventMessageMetric(
            metric_id=vacancy_id,
            column=column,
            action=action,
            entity=EntityEnum.VACANCY_METRIC,
            source="vacancy-metric-service",
            created_at=datetime.now(UTC),
            event_id=str(uuid.uuid4())
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SUM_RED_METRIC_TOPIC)

