from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostUserMetricEntity


class CommentPostUserMetricRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: CommentPostUserMetricEntity) -> None:
        pass

    @abstractmethod
    async def add(self, metric: CommentPostUserMetricEntity) -> CommentPostUserMetricEntity:
        pass