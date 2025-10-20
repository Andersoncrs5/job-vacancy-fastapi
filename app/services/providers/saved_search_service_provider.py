from app.configs.db.database import SavedSearchEntity
from app.repositories.providers.saved_search_repository_provider import SavedSearchReposioryProvider
from app.services.base.saved_search_service_base import SavedSearchServiceBase
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, UpdateSavedSearchDTO
from app.services.generics.generic_service import GenericService
from app.utils.filter.saved_search_filter import SavedSearchFilter
from typing import List
from app.utils.enums.sum_red import SumRedEnum

class SavedSearchServiceProvider(
    SavedSearchServiceBase,
    GenericService[
        SavedSearchEntity,
        SavedSearchReposioryProvider,
        SavedSearchFilter,
    ]
):
    def __init__(self, repository: SavedSearchReposioryProvider):
        super().__init__(repository)

    async def create(self, user_id: int, dto: CreateSavedSearchDTO) -> SavedSearchEntity:
        save = dto.to_entity()
        save.user_id = user_id
        return await self.repository.add(save)

    async def toggle_notifications_enabled(self, save: SavedSearchEntity) -> SavedSearchEntity:
        save.notifications_enabled = not save.notifications_enabled
        return await self.repository.save(save)

    async def toggle_is_public(self, save: SavedSearchEntity) -> SavedSearchEntity:
        save.is_public = not save.is_public
        return await self.repository.save(save)

    async def update(self, save: SavedSearchEntity, dto: UpdateSavedSearchDTO) -> SavedSearchEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(save, field, value)

        return await self.repository.save(save)

    async def sum_or_red_execution_count(self, save: SavedSearchEntity, action: SumRedEnum ) -> SavedSearchEntity:
        if action == SumRedEnum.SUM:
            save.execution_count += 1

        if action == SumRedEnum.RED:
            save.execution_count -= 1

        return await self.repository.save(save)