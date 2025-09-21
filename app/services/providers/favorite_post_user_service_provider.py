from app.services.base.favorite_post_user_service_base import FavoritePostUserServiceBase
from app.configs.db.database import FavoritePostUserEntity, PostUserEntity, UserEntity
from app.repositories.providers.favorite_posts_user_repository_provider import FavoritePostUserRepositoryProvider

class FavoritePostUserServiceProvider(FavoritePostUserServiceBase):
    def __init__(self, repository: FavoritePostUserRepositoryProvider):
        self.repository = repository

    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostUserEntity]:
        return await self.repository.get_all_by_user_id(user_id)

    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostUserEntity]:
        return await self.repository.get_all_by_user_id_just_post(user_id)

    async def exists_by_user_id_post_id(self, user_id: int, post_id: int) -> bool:
        return await self.repository.exists_by_user_id_post_id(user_id, post_id)

    async def get_by_id(self, id: int) -> FavoritePostUserEntity | None:
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)

    async def delete(self, favo: FavoritePostUserEntity):
        await self.repository.delete(favo)

    async def add(self, post: PostUserEntity, user: UserEntity) -> FavoritePostUserEntity:
        favo = FavoritePostUserEntity( user_id = user.id, post_user_id = post.id )

        return await self.repository.add(favo)
    