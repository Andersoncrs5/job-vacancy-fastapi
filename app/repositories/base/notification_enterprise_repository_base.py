from abc import ABC, abstractmethod

from app.configs.db.database import NotificationEnterpriseEntity
from app.utils.filter.notification_enterprise_filter import NotificationEnterpriseFilter


class NotificationEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, _id: int) -> NotificationEnterpriseEntity | None:
        pass

    @abstractmethod
    async def get_all(self, _filter: NotificationEnterpriseFilter) -> NotificationEnterpriseEntity | None:
        pass

    @abstractmethod
    async def add(self, noti: NotificationEnterpriseEntity) -> NotificationEnterpriseEntity:
        pass

    @abstractmethod
    async def save(self, noti: NotificationEnterpriseEntity) -> NotificationEnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, noti: NotificationEnterpriseEntity):
        pass

    @abstractmethod
    async def exists_by_id(self, _id: int) -> bool:
        pass