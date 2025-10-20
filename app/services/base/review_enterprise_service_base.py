from app.configs.db.database import ReviewEnterprise
from abc import ABC, abstractmethod
from typing import List
from app.schemas.review_enterprise_schemas import CreateReviewEnterpriseDTO, UpdateReviewEnterpriseDTO
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter

class ReviewEnterpriseServiceBase(ABC):

    @abstractmethod
    async def update(self, view: ReviewEnterprise, dto: UpdateReviewEnterpriseDTO) -> ReviewEnterprise:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateReviewEnterpriseDTO) -> ReviewEnterprise:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass