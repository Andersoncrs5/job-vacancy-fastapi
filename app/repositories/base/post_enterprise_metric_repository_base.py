from abc import ABC, abstractmethod

from app.configs.db.database import PostEnterpriseMetricEntity


class PostEnterpriseMetricRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: PostEnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def add(self, metric: PostEnterpriseMetricEntity) -> PostEnterpriseMetricEntity:
        pass