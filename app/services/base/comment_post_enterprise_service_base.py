from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseEntity
from app.schemas.comment_post_enterprise_schemas import CreateCommentPostEnterpriseDTO, UpdateCommentPostEnterpriseDTO
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> CommentPostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, comment: CommentPostEnterpriseEntity):
        pass

    @abstractmethod
    async def get_all(self, filter: CommentPostEnterpriseFilter) -> list[CommentPostEnterpriseEntity]:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def update(self, comment: CommentPostEnterpriseEntity, dto: UpdateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        pass
