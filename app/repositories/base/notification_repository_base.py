from abc import ABC, abstractmethod

from app.configs.db.database import NotificationEntity
from app.utils.filter.notification_filter import NotificationFilter


class NotificationRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, _id: int) -> NotificationEntity | None:
        pass

    @abstractmethod
    async def get_all(self, _filter: NotificationFilter) -> NotificationEntity | None:
        pass

    @abstractmethod
    async def add(self, noti: NotificationEntity) -> NotificationEntity:
        pass

    @abstractmethod
    async def save(self, noti: NotificationEntity) -> NotificationEntity:
        pass

    @abstractmethod
    async def delete(self, noti: NotificationEntity):
        pass

    @abstractmethod
    async def exists_by_id(self, _id: int) -> bool:
        pass