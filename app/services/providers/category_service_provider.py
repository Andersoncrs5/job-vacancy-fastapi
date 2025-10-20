from app.services.base.category_service_base import *
from app.configs.db.database import CategoryEntity
from fastapi import HTTPException, status
from app.repositories.providers.category_repository_provider import CategoryRepositoryProvider
from typing import Final
from app.utils.enums.sum_red import SumRedEnum

class CategoryServiceProvider(CategoryServiceBase):
    def __init__(self, repository: CategoryRepositoryProvider):
        self.repository = repository

    async def update(self, category: CategoryEntity, dto: UpdateCategoryDTO) -> CategoryEntity:
        if dto.description != None:
            category.description = dto.description

        if dto.order != None:
            category.order = dto.order

        if dto.icon_url != None:
            category.icon_url = dto.icon_url

        return await self.repository.save(category)

    async def get_by_id(self, id: int) -> CategoryEntity | None:
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)

    async def delete(self, category: CategoryEntity):
        await self.repository.delete(category)
    
    async def exists_by_name(self, name: str) -> bool:
        return await self.repository.exists_by_name(name)

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def toggle_is_active(self, category: CategoryEntity) -> CategoryEntity:
        category.is_active = not category.is_active

        return await self.repository.save(category)

    async def exists_by_slug(self, slug: str) -> bool:
        return await self.repository.exists_by_slug(slug)

    async def sum_red_post_count(self, category: CategoryEntity, action: SumRedEnum) -> CategoryEntity:
        if action == SumRedEnum.SUM:
            category.post_count += category.post_count

        if action == SumRedEnum.RED:
            category.post_count -= category.post_count

        return await self.repository.save(category)

    async def sum_red_job_count(self, category: CategoryEntity, action: SumRedEnum) -> CategoryEntity:
        if action == SumRedEnum.SUM:
            category.job_count += category.job_count

        if action == SumRedEnum.RED:
            category.job_count -= category.job_count

        return await self.repository.save(category)

    async def get_all_filter(self, is_active: bool, filter: CategoryFilter) -> list[CategoryEntity]:
        return await self.repository.get_all(filter)

    async def create(self, user: UserEntity, dto: CreateCategoryDTO) -> CategoryEntity:
        category_mapped: Final = dto.to_category_entity()
        category_mapped.user_id = user.id

        category_created = await self.repository.add(category_mapped)

        return category_created