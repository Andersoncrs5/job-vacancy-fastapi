from abc import ABC, abstractmethod
from typing import TypeVar

from app.configs.db.database import CommentPostUserEntity
from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter

CommentEntity = TypeVar('CommentEntity')
CommentRepo = TypeVar('CommentRepo')
CommentFilter = TypeVar('CommentFilter')

class CommentPostUserServiceBase(ABC):

    @abstractmethod
    async def create(self, user_id: int, dto: CreateCommentPostUserDTO) -> CommentPostUserEntity:
        pass

    @abstractmethod
    async def update(self, comment: CommentPostUserEntity, dto: UpdateCommentPostUserDTO) -> CommentPostUserEntity:
        pass
