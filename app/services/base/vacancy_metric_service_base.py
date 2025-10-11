from abc import ABC, abstractmethod

from app.configs.db.database import VacancyMetricEntity
from app.utils.enums.sum_red import ColumnsVacancyMetricEnum, SumRedEnum


class VacancyMetricServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        pass

    @abstractmethod
    async def update_metric(self, user_id, column: ColumnsVacancyMetricEnum, action: SumRedEnum):
        pass

    @abstractmethod
    async def delete(self, metric: VacancyMetricEntity):
        pass

