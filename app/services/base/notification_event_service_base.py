from abc import ABC, abstractmethod

from app.configs.db.enums import NotificationTypeEnum


class NotificationEventServiceBase(ABC):

    @abstractmethod
    async def notify_event_to_kafka(self, entity_id: int, actor_id: int | None, _type: NotificationTypeEnum,
                                    data: dict):
        pass

    @abstractmethod
    async def notify_user_about(self, entity_id: int, actor_id: int | None, _type: NotificationTypeEnum, data: dict):
        pass