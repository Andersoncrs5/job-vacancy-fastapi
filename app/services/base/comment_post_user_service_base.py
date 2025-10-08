from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostUserEntity
from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserServiceBase(ABC):

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
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateCommentPostUserDTO) -> CommentPostUserEntity:
        pass

    @abstractmethod
    async def update(self, comment: CommentPostUserEntity, dto: UpdateCommentPostUserDTO) -> CommentPostUserEntity:
        pass
