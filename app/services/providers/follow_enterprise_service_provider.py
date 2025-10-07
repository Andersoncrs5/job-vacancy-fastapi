from app.configs.db.database import FollowerRelationshipEnterpriseEntity
from app.repositories.providers.follow_enterprise_repository_provider import FollowEnterpriseRepositoryProvider
from app.services.base.follow_enterprise_service_base import FollowEnterpriseServiceBase


class FollowEnterpriseServiceProvider(FollowEnterpriseServiceBase):
    def __init__(self, repository: FollowEnterpriseRepositoryProvider):
        self.repository = repository

    async def delete(self, follow: FollowerRelationshipEnterpriseEntity):
        await self.repository.delete(follow)

    async def get_by_user_id_and_enterprise_id(
            self, user_id: int, enterprise_id: int
    ) -> FollowerRelationshipEnterpriseEntity | None:
        return await self.repository.get_by_user_id_and_enterprise_id(user_id, enterprise_id)

    async def exists_by_user_id_and_enterprise_id(self, user_id: int, enterprise_id: int) -> bool:
        return await self.repository.exists_by_user_id_and_enterprise_id(user_id, enterprise_id)

    async def get_all_filtered(
            self, user_id: int | None = None, enterprise_id: int | None = None
    ) -> list[FollowerRelationshipEnterpriseEntity]:
        return await self.repository.get_all_filtered(user_id, enterprise_id)

    async def create(self, user_id: int, enterprise_id: int) -> FollowerRelationshipEnterpriseEntity:
        follow = FollowerRelationshipEnterpriseEntity(user_id=user_id, enterprise_id=enterprise_id)

        return await self.repository.add(follow=follow)