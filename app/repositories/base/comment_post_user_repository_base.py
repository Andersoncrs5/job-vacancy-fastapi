from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostUserEntity
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> CommentPostUserEntity | None:
        pass

    @abstractmethod
    async def delete(self, comment: CommentPostUserEntity):
        pass

    @abstractmethod
    async def get_all(self, filter: CommentPostUserFilter) -> list[CommentPostUserEntity]:
        pass

    @abstractmethod
    async def add(self, comment: CommentPostUserEntity) -> CommentPostUserEntity:
        pass

    @abstractmethod
    async def save(self, comment: CommentPostUserEntity) -> CommentPostUserEntity:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass

