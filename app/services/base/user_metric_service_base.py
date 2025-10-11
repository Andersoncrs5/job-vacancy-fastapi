from abc import ABC, abstractmethod

from app.configs.db.database import UserMetricEntity
from app.utils.enums.sum_red import SumRedEnum, ColumnUserMetricEnum


class UserMetricServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserMetricEntity | None:
        pass

    @abstractmethod
    async def create(self, user_id: int) -> UserMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: UserMetricEntity):
        pass

    @abstractmethod
    async def update_metric_v2(self, user_id, column: ColumnUserMetricEnum, action: SumRedEnum):
        pass

    @abstractmethod
    async def update_metric(self, metric: UserMetricEntity, column: ColumnUserMetricEnum, action: SumRedEnum):
        pass
