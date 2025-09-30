from abc import ABC, abstractmethod
from app.configs.db.database import AreaEntity
from app.utils.filter.area_filter import AreaFilter
from typing import List

class AreaRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: AreaFilter) -> List[AreaEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> AreaEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def save(self, area: AreaEntity) -> AreaEntity:
        pass

    @abstractmethod
    async def add(self, area: AreaEntity) -> AreaEntity:
        pass

    @abstractmethod
    async def delete(self, area: AreaEntity):
        pass