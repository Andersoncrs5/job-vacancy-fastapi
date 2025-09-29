from abc import ABC, abstractmethod
from typing import List
from app.configs.db.database import ReviewEnterprise
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter

class ReviewEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: ReviewEnterpriseFilter) -> List[ReviewEnterprise]:
        pass

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
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def exists_by_user_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> ReviewEnterprise | None:
        pass