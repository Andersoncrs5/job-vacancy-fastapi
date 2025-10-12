from abc import ABC, abstractmethod

from app.configs.db.database import EnterpriseMetricEntity
from app.utils.enums.sum_red import SumRedEnum, ColumnEnterpriseMetricEnum


class EnterpriseMetricServiceBase(ABC):

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
    async def create(self, enterprise_id: int) -> None:
        pass

    @abstractmethod
    async def update_metric(self, metric: EnterpriseMetricEntity, column: ColumnEnterpriseMetricEnum, action: SumRedEnum):
        pass