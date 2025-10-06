from app.configs.db.database import FollowerRelationshipEntity
from app.repositories.providers.follow_repository_provider import FollowRepositoryProvider
from app.services.base.follow_service_base import FollowServiceBase


class FollowServiceProvider(FollowServiceBase):
    def __init__(self, repository: FollowRepositoryProvider):
        self.repository = repository

    async def delete(self, follow: FollowerRelationshipEntity):
        await self.repository.delete(follow)

    async def create(self, user_id: int, followed_id: int) -> FollowerRelationshipEntity:
        follow = FollowerRelationshipEntity(followed_id=followed_id, follower_id = user_id)
        return await self.repository.add(follow)

    async def get_by_follower_id_and_followed_id(self, user_id: int,
                                                 followed_id: int) -> FollowerRelationshipEntity | None:
        return await self.repository.get_by_follower_id_and_followed_id(user_id, followed_id)

    async def exists_by_follower_id_and_followed_id(self, user_id: int, followed_id: int) -> bool:
        return await self.repository.exists_by_follower_id_and_followed_id(user_id, followed_id)

    async def get_all(self, user_id: int) -> list[FollowerRelationshipEntity]:
        return await self.repository.get_all(user_id)