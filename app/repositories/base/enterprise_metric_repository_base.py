from abc import ABC, abstractmethod

from app.configs.db.database import EnterpriseMetricEntity


class EnterpriseMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        pass

    @abstractmethod
    async def exists_by_id(self, enterprise_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, metric: EnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def add(self, metric: EnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def save(self, metric: EnterpriseMetricEntity) -> EnterpriseMetricEntity:
        pass