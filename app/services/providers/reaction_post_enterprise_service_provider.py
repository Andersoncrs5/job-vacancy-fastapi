from app.configs.db.database import ReactionPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum
from app.repositories.providers.reaction_post_enterprise_provider import ReactionPostEnterpriseRepositoryProvider
from app.schemas.reaction_post_enterprise_schemas import CreateReactionPostEnterpriseDTO
from app.services.base.reaction_post_enterprise_service_base import ReactionPostEnterpriseServiceBase


class ReactionPostEnterpriseServiceProvider(ReactionPostEnterpriseServiceBase):
    def __init__(self, repository: ReactionPostEnterpriseRepositoryProvider):
        self.repository = repository

    async def get_by_user_id_and_post_enterprise_id(
            self, user_id: int, post_enterprise_id: int
    ) -> ReactionPostEnterpriseEntity | None:
        return await self.repository.get_by_user_id_and_post_enterprise_id(user_id, post_enterprise_id)

    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        return await self.repository.exists_by_user_id_and_post_enterprise_id(user_id, post_enterprise_id)

    async def delete(self, reaction: ReactionPostEnterpriseEntity):
        await self.repository.delete(reaction=reaction)

    async def get_all(self, user_id: int | None, post_enterprise_id: int | None) -> list[ReactionPostEnterpriseEntity]:
        return await self.repository.get_all(user_id=user_id, post_enterprise_id=post_enterprise_id)

    async def create(self, user_id, dto: CreateReactionPostEnterpriseDTO) -> ReactionPostEnterpriseEntity:
        react = ReactionPostEnterpriseEntity(
            user_id=user_id,
            post_enterprise_id=dto.post_enterprise_id,
            reaction_type=dto.reaction_type,
        )

        return await self.repository.add(react)

    async def toggle_reaction_type(self, reaction: ReactionPostEnterpriseEntity) -> ReactionPostEnterpriseEntity:
        if reaction.reaction_type == ReactionTypeEnum.LIKE:
            reaction.reaction_type = ReactionTypeEnum.DISLIKE

        if reaction.reaction_type == ReactionTypeEnum.DISLIKE:
            reaction.reaction_type = ReactionTypeEnum.LIKE

        return await self.repository.save(reaction)