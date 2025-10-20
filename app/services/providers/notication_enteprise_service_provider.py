from app.configs.db.database import NotificationEnterpriseEntity
from app.repositories.providers.notification_enterprise_repository_provider import NotificationEnterpriseRepositoryProvider
from app.services.base.notication_enterprise_service_base import NotificationEnterpriseServiceBase
from app.utils.filter.notification_enterprise_filter import NotificationEnterpriseFilter


class NotificationEnterpriseServiceProvider(NotificationEnterpriseServiceBase):
    def __init__(self, repository: NotificationEnterpriseRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, _id: int) -> NotificationEnterpriseEntity | None:
        return await self.repository.get_by_id(_id)

    async def get_all(self, _filter: NotificationEnterpriseFilter) -> list[NotificationEnterpriseEntity]:
        return await self.repository.get_all(_filter)

    async def delete(self, noti: NotificationEnterpriseEntity):
        await self.repository.delete(noti)

    async def toggle_is_view(self, noti: NotificationEnterpriseEntity):
        noti.is_view = not noti.is_view
        return await self.repository.save(noti)

    async def exists_by_id(self, _id: int) -> bool:
        return await self.repository.exists_by_id(_id)