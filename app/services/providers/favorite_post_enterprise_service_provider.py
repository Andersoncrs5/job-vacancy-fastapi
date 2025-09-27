from app.services.base.favorite_post_enterprise_service_base import FavoritePostEnterpriseServiceBase
from app.configs.db.database import FavoritePostEnterpriseEntity, PostEnterpriseEntity, EnterpriseEntity, UserEntity
from app.repositories.providers.favorite_posts_enterprise_repository_provider import FavoritePostEnterpriseRepositoryProvider

class FavoritePostEnterpriseServiceProvider(FavoritePostEnterpriseServiceBase):
    def __init__(self, repository: FavoritePostEnterpriseRepositoryProvider):
        self.repository = repository

    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        return await self.repository.exists_by_user_id_and_post_enterprise_id(user_id, post_enterprise_id)

    async def get_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> FavoritePostEnterpriseEntity | None:
        return await self.repository.get_by_user_id_and_post_enterprise_id(user_id, post_enterprise_id)

    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostEnterpriseEntity]:
        return await self.repository.get_all_by_user_id(user_id)

    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostEnterpriseEntity]:
        return await self.repository.get_all_by_user_id_just_post(user_id)

    async def get_by_id(self, id: int) -> FavoritePostEnterpriseEntity | None:
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)

    async def delete(self, favo: FavoritePostEnterpriseEntity):
        await self.repository.delete(favo)

    async def add(self, post: PostEnterpriseEntity, user: UserEntity) -> FavoritePostEnterpriseEntity:
        favo = FavoritePostEnterpriseEntity( 
            user_id = user.id,
            post_enterprise_id = post.id,
        )

        return await self.repository.add(favo)
    