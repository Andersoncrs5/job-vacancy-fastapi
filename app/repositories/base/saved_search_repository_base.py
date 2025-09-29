from abc import ABC, abstractmethod
from app.configs.db.database import SavedSearchEntity
from app.utils.filter.saved_search_filter import SavedSearchFilter
from typing import List

class SavedSearchReposioryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: SavedSearchFilter) -> List[SavedSearchEntity]:
        pass

    @abstractmethod
    async def delete(self, save: SavedSearchEntity):
        pass

    @abstractmethod
    async def add(self, save: SavedSearchEntity) -> SavedSearchEntity:
        pass

    @abstractmethod
    async def save(self, save: SavedSearchEntity) -> SavedSearchEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> SavedSearchEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass