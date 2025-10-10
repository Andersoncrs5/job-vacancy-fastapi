from abc import ABC, abstractmethod

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.schemas.reaction_comment_post_enterprise_schemas import CreateReactionCommentPostEnterpriseDTO
from app.utils.filter.reaction_comment_post_enterprise_filter import ReactionCommentPostEnterpriseFilter


class ReactionCommentPostEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_all(
            self,
            filter: ReactionCommentPostEnterpriseFilter
    ) -> list[ReactionCommentPostEnterpriseEntity]:
        pass

    @abstractmethod
    async def get_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> ReactionCommentPostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> bool:
        pass

    @abstractmethod
    async def delete(self, react: ReactionCommentPostEnterpriseEntity):
        pass

    @abstractmethod
    async def create(
            self,
            user_id: int,
            dto: CreateReactionCommentPostEnterpriseDTO
    ) -> ReactionCommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def toggle_reaction_type(
            self,
            react: ReactionCommentPostEnterpriseEntity
    ) -> ReactionCommentPostEnterpriseEntity:
        pass