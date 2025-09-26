from abc import ABC, abstractmethod
from app.configs.db.database import SkillEntity
from app.utils.filter.skill_filter import SkillFilter
from typing import List

class SkillRepositoryBase(ABC):

    @abstractmethod
    async def add(self, skill: SkillEntity) -> SkillEntity:
        pass
    
    @abstractmethod
    async def save(self, skill: SkillEntity) -> SkillEntity:
        pass

    @abstractmethod
    async def get_all(self, filter: SkillFilter) -> List[SkillEntity]:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> (SkillEntity | None):
        pass

    @abstractmethod
    async def delete(self, skill: SkillEntity):
        pass