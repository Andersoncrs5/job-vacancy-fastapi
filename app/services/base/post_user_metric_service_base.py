from abc import ABC, abstractmethod

from app.configs.db.database import PostUserMetricEntity


class PostUserMetricServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: PostUserMetricEntity) -> None:
        pass

    @abstractmethod
    async def create(self, post_id) -> PostUserMetricEntity:
        pass