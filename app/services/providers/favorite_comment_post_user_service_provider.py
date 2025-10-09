from app.configs.db.database import FavoriteCommentPostUserEntity
from app.repositories.providers.favorite_comment_post_user_repository_provider import \
    FavoriteCommentPostUserRepositoryProvider
from app.services.base.favorite_comment_post_user_service_base import FavoriteCommentPostUserServiceBase


class FavoriteCommentPostUserServiceProvider(FavoriteCommentPostUserServiceBase):
    def __init__(self, repository: FavoriteCommentPostUserRepositoryProvider):
        self.repository = repository

    async def create(self, user_id: int, comment_user_id: int) -> FavoriteCommentPostUserEntity:
        favor = FavoriteCommentPostUserEntity(user_id=user_id, comment_user_id=comment_user_id)

        return await self.repository.add(favor)

    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        return await self.repository.exists_by_user_id_and_comment_user_id(user_id, comment_user_id)

    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> FavoriteCommentPostUserEntity | None:
        return await self.repository.get_by_user_id_and_comment_user_id(user_id, comment_user_id)

    async def get_all(
            self, user_id: int | None, comment_user_id: int | None
    ) -> list[FavoriteCommentPostUserEntity]:
        return await self.repository.get_all(user_id, comment_user_id)

    async def delete(self, favor: FavoriteCommentPostUserEntity):
        await self.repository.delete(favor)