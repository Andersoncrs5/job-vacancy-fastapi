from abc import ABC, abstractmethod
from app.configs.db.database import AreaEntity
from app.utils.filter.area_filter import AreaFilter
from typing import List
from app.schemas.area_schemas import UpdateAreaDTO, CreateAreaDTO

class AreaServiceBase(ABC):

    @abstractmethod
    async def toggle_is_active(self, area: AreaEntity) -> AreaEntity:
        pass

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
    async def update(self, area: AreaEntity, dto: UpdateAreaDTO) -> AreaEntity:
        pass

    @abstractmethod
    async def create(self, user_id: int, dto: CreateAreaDTO) -> AreaEntity:
        pass

    @abstractmethod
    async def delete(self, area: AreaEntity):
        pass