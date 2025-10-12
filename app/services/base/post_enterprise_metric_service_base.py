from abc import ABC, abstractmethod

from app.configs.db.database import PostEnterpriseMetricEntity
from app.utils.enums.sum_red import SumRedEnum, ColumnsPostEnterpriseMetricEnum


class PostEnterpriseMetricServiceBase(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: PostEnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def update_metric(self, post_id, column: ColumnsPostEnterpriseMetricEnum, action: SumRedEnum):
        pass

    @abstractmethod
    async def create(self, post_id: int) -> PostEnterpriseMetricEntity:
        pass