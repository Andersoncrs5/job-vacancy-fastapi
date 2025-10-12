from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseMetricEntity


class CommentPostEnterpriseMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: CommentPostEnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def add(self, metric: CommentPostEnterpriseMetricEntity) -> CommentPostEnterpriseMetricEntity:
        pass