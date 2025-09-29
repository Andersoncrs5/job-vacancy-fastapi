from app.services.base.review_enterprise_service_base import ReviewEnterpriseServiceBase
from app.repositories.providers.review_enterprise_repository_provider import ReviewEnterpriseRepositoryProvider
from typing import List
from app.schemas.review_enterprise_schemas import CreateReviewEnterpriseDTO, UpdateReviewEnterpriseDTO
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter
from app.configs.db.database import ReviewEnterprise

class ReviewEnterpriseServiceProvider(ReviewEnterpriseRepositoryProvider):
    def __init__(self, repository: ReviewEnterpriseRepositoryProvider):
        self.repository = repository

    async def update(self, view: ReviewEnterprise, dto: UpdateReviewEnterpriseDTO) -> ReviewEnterprise:
        if dto.rating != None:
            view.rating = dto.rating

        if dto.title != None:
            view.title = dto.title

        if dto.pros != None:
            view.pros = dto.pros

        if dto.cons != None:
            view.cons = dto.cons

        if dto.would_recommend != None:
            view.would_recommend = dto.would_recommend

        if dto.position != None:
            view.position = dto.position

        if dto.salary_range != None:
            view.salary_range = dto.salary_range

        if dto.employment_type != None:
            view.employment_type = dto.employment_type

        if dto.employment_status != None:
            view.employment_status = dto.employment_status

        return await self.repository.save(view)

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
        