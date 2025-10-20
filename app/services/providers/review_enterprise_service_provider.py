from app.services.base.review_enterprise_service_base import ReviewEnterpriseServiceBase
from app.repositories.providers.review_enterprise_repository_provider import ReviewEnterpriseRepositoryProvider
from typing import List
from app.schemas.review_enterprise_schemas import CreateReviewEnterpriseDTO, UpdateReviewEnterpriseDTO
from app.services.generics.generic_service import GenericService
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter
from app.configs.db.database import ReviewEnterprise

class ReviewEnterpriseServiceProvider(
    ReviewEnterpriseServiceBase,
    GenericService[
        ReviewEnterprise,
        ReviewEnterpriseRepositoryProvider,
        ReviewEnterpriseFilter
    ]
):
    def __init__(self, repository: ReviewEnterpriseRepositoryProvider):
        super().__init__(repository)

    async def update(self, view: ReviewEnterprise, dto: UpdateReviewEnterpriseDTO) -> ReviewEnterprise:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(view, field, value)

        return await self.repository.save(view)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def create(self, user_id: int, dto: CreateReviewEnterpriseDTO) -> ReviewEnterprise:
        view = dto.to_entity()
        view.user_id = user_id

        return await self.repository.add(view)
        