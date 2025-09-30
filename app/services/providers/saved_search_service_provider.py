from app.configs.db.database import SavedSearchEntity
from app.repositories.providers.saved_search_repository_provider import SavedSearchReposioryProvider
from app.services.base.saved_search_service_base import SavedSearchServiceBase
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, UpdateSavedSearchDTO
from app.utils.filter.saved_search_filter import SavedSearchFilter
from typing import List
from app.utils.enums.sum_red import SumRedEnum

class SavedSearchServiceProvider(SavedSearchServiceBase):
    def __init__(self, repository: SavedSearchReposioryProvider):
        self.repository = repository

    async def delete(self, save: SavedSearchEntity):
        await self.repository.delete(save)

    async def get_by_id(self, id: int) -> (SavedSearchEntity | None):
        return await self.repository.get_by_id(id)

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
        if dto.name != None:
            save.name = dto.name

        if dto.query != None:
            save.query = dto.query

        if dto.description != None:
            save.description = dto.description

        if dto.is_public != None:
            save.is_public = dto.is_public

        if dto.is_public != None:
            save.is_public = dto.is_public

        if dto.last_executed_at != None:
            save.last_executed_at = dto.last_executed_at

        if dto.notifications_enabled != None:
            save.notifications_enabled = dto.notifications_enabled

        return await self.repository.save(save)

    async def get_all(self, filter: SavedSearchFilter) -> List[SavedSearchEntity]:
        return await self.repository.get_all(filter)
        
    async def sum_or_red_execution_count(self, save: SavedSearchEntity, action: SumRedEnum ) -> SavedSearchEntity:
        if action == SumRedEnum.SUM:
            save.execution_count += 1

        if action == SumRedEnum.RED:
            save.execution_count -= 1

        return await self.repository.save(save)