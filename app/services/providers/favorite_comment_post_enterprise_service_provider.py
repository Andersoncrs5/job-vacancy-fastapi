from app.configs.db.database import FavoriteCommentPostEnterpriseEntity
from app.repositories.providers.favorite_comment_post_enterprise_repository_provider import \
    FavoriteCommentPostEnterpriseRepositoryProvider
from app.services.base.favorite_comment_post_enterprise_service_base import FavoriteCommentPostEnterpriseServiceBase


class FavoriteCommentPostEnterpriseServiceProvider(FavoriteCommentPostEnterpriseServiceBase):
    def __init__(self, repository: FavoriteCommentPostEnterpriseRepositoryProvider):
        self.repository = repository

    async def create(self, user_id: int, comment_enterprise_id: int) -> FavoriteCommentPostEnterpriseEntity:
        favor = FavoriteCommentPostEnterpriseEntity(
            user_id=user_id,
            comment_enterprise_id=comment_enterprise_id,
        )

        return await self.repository.add(favor=favor)

    async def exists_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> bool:
        return await self.repository.exists_by_user_id_and_comment_enterprise_id(user_id, comment_enterprise_id)

    async def get_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> FavoriteCommentPostEnterpriseEntity | None:
        return await self.repository.get_by_user_id_and_comment_enterprise_id(user_id, comment_enterprise_id)

    async def get_all(
            self, user_id: int | None, comment_enterprise_id: int | None
    ) -> list[FavoriteCommentPostEnterpriseEntity]:
        return await self.repository.get_all(user_id, comment_enterprise_id)

    async def delete(self, favor: FavoriteCommentPostEnterpriseEntity):
        await self.repository.delete(favor)