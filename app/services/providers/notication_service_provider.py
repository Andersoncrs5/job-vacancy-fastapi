from app.configs.db.database import NotificationEntity
from app.repositories.providers.notification_repository_provider import NotificationRepositoryProvider
from app.services.base.notication_service_base import NotificationServiceBase
from app.utils.filter.notification_filter import NotificationFilter


class NotificationServiceProvider(NotificationServiceBase):
    def __init__(self, repository: NotificationRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, _id: int) -> NotificationEntity | None:
        return await self.repository.get_by_id(_id)

    async def get_all(self, _filter: NotificationFilter) -> list[NotificationEntity]:
        return await self.repository.get_all(_filter)

    async def delete(self, noti: NotificationEntity):
        await self.repository.delete(noti)

    async def exists_by_id(self, _id: int) -> bool:
        return await self.repository.exists_by_id(_id)