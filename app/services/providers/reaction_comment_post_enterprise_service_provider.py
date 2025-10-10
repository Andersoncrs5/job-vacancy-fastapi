from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum
from app.repositories.providers.reaction_comment_post_enterprise_repository_provider import \
    ReactionCommentPostEnterpriseRepositoryProvider
from app.schemas.reaction_comment_post_enterprise_schemas import CreateReactionCommentPostEnterpriseDTO
from app.services.base.reaction_comment_post_enterprise_service_base import ReactionCommentPostEnterpriseServiceBase
from app.utils.filter.reaction_comment_post_enterprise_filter import ReactionCommentPostEnterpriseFilter


class ReactionCommentPostEnterpriseServiceProvider(ReactionCommentPostEnterpriseServiceBase):
    def __init__(self, repository: ReactionCommentPostEnterpriseRepositoryProvider):
        self.repository = repository

    async def get_all(
            self,
            filter: ReactionCommentPostEnterpriseFilter
    ) -> list[ReactionCommentPostEnterpriseEntity]:
        return await self.repository.get_all(filter)

    async def get_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> ReactionCommentPostEnterpriseEntity | None:
        return await self.repository.get_by_user_id_and_comment_enterprise_id(user_id, comment_enterprise_id)

    async def exists_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> bool:
        return await self.repository.exists_by_user_id_and_comment_enterprise_id(user_id, comment_enterprise_id)

    async def delete(self, react: ReactionCommentPostEnterpriseEntity):
        await self.repository.delete(react)

    async def create(
            self,
            user_id: int,
            dto: CreateReactionCommentPostEnterpriseDTO
    ) -> ReactionCommentPostEnterpriseEntity:
        react = ReactionCommentPostEnterpriseEntity(
            user_id=user_id,
            comment_enterprise_id=dto.comment_enterprise_id,
            reaction_type=dto.reaction_type,
        )

        return await self.repository.add(react)

    async def toggle_reaction_type(
            self,
            react: ReactionCommentPostEnterpriseEntity
    ) -> ReactionCommentPostEnterpriseEntity:
        if react.reaction_type == ReactionTypeEnum.LIKE:
            react.reaction_type = ReactionTypeEnum.DISLIKE

        if react.reaction_type == ReactionTypeEnum.DISLIKE:
            react.reaction_type = ReactionTypeEnum.LIKE

        return await self.repository.save(react)