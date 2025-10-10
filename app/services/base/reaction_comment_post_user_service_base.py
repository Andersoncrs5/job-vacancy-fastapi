from abc import ABC, abstractmethod

from app.configs.db.database import ReactionCommentPostUserEntity
from app.schemas.reaction_comment_post_user_schemas import CreateReactionCommentPostUserDTO


class ReactionCommentPostUserServiceBase(ABC):

    @abstractmethod
    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> ReactionCommentPostUserEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateReactionCommentPostUserDTO) -> ReactionCommentPostUserEntity:
        pass

    @abstractmethod
    async def delete(self, react: ReactionCommentPostUserEntity):
        pass

    @abstractmethod
    async def toggle_reaction_type(self, react :ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        pass