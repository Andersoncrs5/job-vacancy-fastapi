from app.configs.db.database import ReactionPostUserEntity
from app.configs.db.enums import ReactionTypeEnum
from app.repositories.providers.reaction_post_user_repository_provider import ReactionPostUserRepositoryProvider
from app.schemas.reaction_post_user_schemas import CreateReactionPostUserDTO
from app.services.base.reaction_post_user_service_base import ReactionPostUserServiceBase


class ReactionPostUserServiceProvider(ReactionPostUserServiceBase):
    def __init__(self, repository: ReactionPostUserRepositoryProvider):
        self.repository = repository

    async def get_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> ReactionPostUserEntity | None:
        return await self.repository.get_by_user_id_and_post_user_id(user_id, post_user_id)

    async def exists_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> bool:
        return await self.repository.exists_by_user_id_and_post_user_id(user_id, post_user_id)

    async def get_all(self, user_id: int | None, post_user_id: int | None) -> list[ReactionPostUserEntity]:
        return await self.repository.get_all(user_id, post_user_id)

    async def create(self, user_id: int, dto: CreateReactionPostUserDTO) -> ReactionPostUserEntity:
        reaction = ReactionPostUserEntity(
            user_id=user_id,
            post_user_id=dto.post_user_id,
            reaction_type=dto.reaction_type
        )

        return await self.repository.add(reaction)

    async def delete(self, reaction: ReactionPostUserEntity):
        await self.repository.delete(reaction)

    async def toggle_reaction_type(self, reaction: ReactionPostUserEntity) -> ReactionPostUserEntity:
        if reaction.reaction_type == ReactionTypeEnum.LIKE:
            reaction.reaction_type = ReactionTypeEnum.DISLIKE

        if reaction.reaction_type == ReactionTypeEnum.DISLIKE:
            reaction.reaction_type = ReactionTypeEnum.LIKE

        return await self.repository.save(reaction)