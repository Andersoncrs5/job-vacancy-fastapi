from app.configs.db.database import SavedSearchEntity
from abc import ABC, abstractmethod
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, UpdateSavedSearchDTO
from app.utils.filter.saved_search_filter import SavedSearchFilter
from typing import List
from app.utils.enums.sum_red import SumRedEnum

class SavedSearchServiceBase(ABC):

    @abstractmethod
    async def toggle_is_public(self, save: SavedSearchEntity) -> SavedSearchEntity:
        pass
    
    @abstractmethod
    async def sum_or_red_execution_count(self, save: SavedSearchEntity, action: SumRedEnum ) -> SavedSearchEntity:
        pass

    @abstractmethod
    async def get_all(self, filter: SavedSearchFilter) -> List[SavedSearchEntity]:
        pass

    @abstractmethod
    async def update(self, save: SavedSearchEntity, dto: UpdateSavedSearchDTO) -> SavedSearchEntity:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateSavedSearchDTO) -> SavedSearchEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> (SavedSearchEntity | None):
        pass

    @abstractmethod
    async def delete(self, save: SavedSearchEntity):
        pass