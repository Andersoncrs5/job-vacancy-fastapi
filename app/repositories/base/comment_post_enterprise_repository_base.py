from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseEntity
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseRepositoryBase(ABC):

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
    async def add(self, comment: CommentPostEnterpriseEntity) -> CommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def save(self, comment: CommentPostEnterpriseEntity) -> CommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
