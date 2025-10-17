from abc import ABC, abstractmethod

from app.configs.db.database import NotificationEntity
from app.utils.filter.notification_filter import NotificationFilter


class NotificationServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, _id: int) -> NotificationEntity | None:
        pass

    @abstractmethod
    async def delete(self, noti: NotificationEntity):
        pass

    @abstractmethod
    async def toggle_is_view(self, noti: NotificationEntity):
        pass

    @abstractmethod
    async def get_all(self, _filter: NotificationFilter) -> list[NotificationEntity]:
        pass