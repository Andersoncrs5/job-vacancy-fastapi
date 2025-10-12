from app.configs.db.database import EnterpriseFollowsUserEntity
from app.repositories.providers.enterprise_follows_user_repository_provider import \
    EnterpriseFollowsUserRepositoryProvider
from app.services.base.enterprise_follows_user_service_base import EnterpriseFollowsUserServiceBase
from app.utils.filter.enterprise_follows_user_filter import EnterpriseFollowsUserFilter


class EnterpriseFollowsUserServiceProvider(EnterpriseFollowsUserServiceBase):
    def __init__(self, repository: EnterpriseFollowsUserRepositoryProvider):
        self.repository = repository

    async def get_all(self, filter: EnterpriseFollowsUserFilter):
        return await self.repository.get_all(filter)

    async def create(self, enterprise_id: int, user_id: int) -> EnterpriseFollowsUserEntity:
        follow = EnterpriseFollowsUserEntity(
            enterprise_id=enterprise_id,
            user_id=user_id,
        )

        return await self.repository.add(follow)

    async def delete(self, follow: EnterpriseFollowsUserEntity):
        await self.repository.delete(follow)

    async def get_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> EnterpriseFollowsUserEntity | None:
        return await self.repository.get_by_enterprise_id_and_user_id(enterprise_id=enterprise_id, user_id=user_id)

    async def exists_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> bool:
        return await self.repository.exists_by_enterprise_id_and_user_id(enterprise_id=enterprise_id, user_id=user_id)