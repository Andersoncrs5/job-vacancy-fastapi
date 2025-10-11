from abc import ABC, abstractmethod

from app.configs.db.database import VacancyMetricEntity


class VacancyMetricRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: VacancyMetricEntity) -> VacancyMetricEntity:
        pass

    @abstractmethod
    async def add(self, metric: VacancyMetricEntity) -> VacancyMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: VacancyMetricEntity):
        pass