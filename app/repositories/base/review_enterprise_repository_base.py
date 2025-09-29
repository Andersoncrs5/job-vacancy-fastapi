from abc import ABC, abstractmethod

from app.configs.db.database import ReviewEnterprise


class ReviewEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def add(self, view: ReviewEnterprise):
        pass

    @abstractmethod
    async def save(self, view: ReviewEnterprise):
        pass

    @abstractmethod
    async def delete(self, view: ReviewEnterprise):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> ReviewEnterprise | None:
        pass