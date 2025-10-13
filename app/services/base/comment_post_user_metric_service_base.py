from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostUserMetricEntity


class CommentPostUserMetricServiceBase(ABC):

    @abstractmethod
    async def delete(self, metric: CommentPostUserMetricEntity) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        pass

    @abstractmethod
    async def create(self, comment_id: int) -> CommentPostUserMetricEntity:
        pass

