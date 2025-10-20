from abc import ABC, abstractmethod

from app.configs.db.database import NotificationEnterpriseEntity
from app.utils.filter.notification_enterprise_filter import NotificationEnterpriseFilter


class NotificationEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, _id: int) -> NotificationEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, noti: NotificationEnterpriseEntity):
        pass

    @abstractmethod
    async def toggle_is_view(self, noti: NotificationEnterpriseEntity):
        pass

    @abstractmethod
    async def get_all(self, _filter: NotificationEnterpriseFilter) -> list[NotificationEnterpriseEntity]:
        pass