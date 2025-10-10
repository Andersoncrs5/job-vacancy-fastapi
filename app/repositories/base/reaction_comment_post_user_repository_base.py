import uuid
from abc import abstractmethod, ABC

from app.configs.db.database import ReactionCommentPostUserEntity
from app.configs.db.enums import ReactionTypeEnum


class ReactionCommentPostUserRepositoryBase(ABC):
    @abstractmethod
    async def get_all(
            self, user_id: int | None,
            comment_user_id: int | None, reaction_type: ReactionTypeEnum | None
    ) -> list[ReactionCommentPostUserEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> ReactionCommentPostUserEntity | None:
        pass

    @abstractmethod
    async def get_by_user_id_and_comment_user_id(self, user_id: int,
                                                 comment_user_id: int) -> ReactionCommentPostUserEntity | None:
        pass

    @abstractmethod
    async def save(self, react: ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        pass

    @abstractmethod
    async def delete(self, react: ReactionCommentPostUserEntity):
        pass

    @abstractmethod
    async def add(self, react: ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_user_id(self, user_id: int,
                                                    comment_user_id: int) -> bool:
        pass
