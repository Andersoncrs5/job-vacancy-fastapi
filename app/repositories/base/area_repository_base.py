from abc import ABC, abstractmethod
from app.configs.db.database import AreaEntity
from app.utils.filter.area_filter import AreaFilter
from typing import List

class AreaRepositoryBase(ABC):
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass