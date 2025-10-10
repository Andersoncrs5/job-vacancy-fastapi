from app.configs.db.database import ReactionCommentPostUserEntity
from app.configs.db.enums import ReactionTypeEnum
from app.repositories.providers.reaction_comment_post_user_repository_provider import \
    ReactionCommentPostUserRepositoryProvider
from app.schemas.reaction_comment_post_user_schemas import CreateReactionCommentPostUserDTO
from app.services.base.reaction_comment_post_user_service_base import ReactionCommentPostUserServiceBase


class ReactionCommentPostUserServiceProvider(ReactionCommentPostUserServiceBase):
    def __init__(self, repository: ReactionCommentPostUserRepositoryProvider):
        self.repository = repository

    async def get_all(
            self,
            user_id: int | None,
            comment_user_id: int | None,
            reaction_type: ReactionTypeEnum | None
    ) -> list[ReactionCommentPostUserEntity]:
        return await self.repository.get_all(user_id,comment_user_id,reaction_type)

    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> ReactionCommentPostUserEntity | None:
        return await self.repository.get_by_user_id_and_comment_user_id(user_id=user_id, comment_user_id=comment_user_id)

    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        return await self.repository.exists_by_user_id_and_comment_user_id(user_id, comment_user_id)

    async def create(self, user_id: int, dto: CreateReactionCommentPostUserDTO) -> ReactionCommentPostUserEntity:
        react = ReactionCommentPostUserEntity(
            user_id=user_id,
            comment_user_id=dto.comment_user_id,
            reaction_type=dto.reaction_type
        )

        return await self.repository.add(react)

    async def delete(self, react: ReactionCommentPostUserEntity):
        await self.repository.delete(react)

    async def toggle_reaction_type(self, react: ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        if react.reaction_type == ReactionTypeEnum.LIKE:
            react.reaction_type = ReactionTypeEnum.DISLIKE

        if react.reaction_type == ReactionTypeEnum.DISLIKE:
            react.reaction_type = ReactionTypeEnum.LIKE

        return await self.repository.save(react)