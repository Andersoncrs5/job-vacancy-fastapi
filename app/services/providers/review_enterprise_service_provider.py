from app.services.base.review_enterprise_service_base import ReviewEnterpriseServiceBase
from app.repositories.providers.review_enterprise_repository_provider import ReviewEnterpriseRepositoryProvider
from typing import List
from app.schemas.review_enterprise_schemas import CreateReviewEnterpriseDTO
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter
from app.configs.db.database import ReviewEnterprise

class ReviewEnterpriseServiceProvider(ReviewEnterpriseRepositoryProvider):
    def __init__(self, repository: ReviewEnterpriseRepositoryProvider):
        self.repository = repository

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def exists_by_id(self, id: int) -> bool :
        return await self.repository.exists_by_id(id)

    async def get_by_id(self, id: int) -> ReviewEnterprise | None:
        return await self.repository.get_by_id(id)
    
    async def delete(self, view: ReviewEnterprise):
        await self.repository.delete(view)

    async def get_all(self, filter: ReviewEnterpriseFilter) -> List[ReviewEnterprise]:
        return await self.repository.get_all(filter)

    async def create(self, user_id: int, dto: CreateReviewEnterpriseDTO) -> ReviewEnterprise:
        view = dto.to_entity()
        view.user_id = user_id

        return await self.repository.add(view)
        