from app.configs.db.database import ReviewEnterprise
from abc import ABC, abstractmethod
from typing import List
from app.schemas.review_enterprise_schemas import CreateReviewEnterpriseDTO
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter

class ReviewEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_all(self, filter: ReviewEnterpriseFilter) -> List[ReviewEnterprise]:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateReviewEnterpriseDTO) -> ReviewEnterprise:
        pass

    @abstractmethod
    async def delete(self, view: ReviewEnterprise):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> ReviewEnterprise | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool :
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass