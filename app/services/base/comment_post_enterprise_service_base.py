from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseEntity
from app.schemas.comment_post_enterprise_schemas import CreateCommentPostEnterpriseDTO, UpdateCommentPostEnterpriseDTO
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseServiceBase(ABC):

    @abstractmethod
    async def create(self, user_id: int, dto: CreateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def update(self, comment: CommentPostEnterpriseEntity, dto: UpdateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        pass
