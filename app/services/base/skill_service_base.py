from abc import ABC , abstractmethod 
from typing import Final
from app.utils.filter.skill_filter import SkillFilter
from app.configs.db.database import SkillEntity
from typing import List
from datetime import datetime
from app.schemas.skill_schemas import SkillOUT, CreateSkillDTO, UpdateSkillDTO

class SkillServiceBase(ABC):

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, filter: SkillFilter) -> List[SkillEntity]:
        pass
    
    @abstractmethod
    async def update(self, skill: SkillEntity, dto: UpdateSkillDTO) -> SkillEntity:
        pass

    @abstractmethod
    async def toggle_is_active(self, skill: SkillEntity) -> SkillEntity: 
        pass
    
    @abstractmethod
    async def create(self, dto: CreateSkillDTO) -> SkillEntity:
        pass

    @abstractmethod
    async def delete(self, skill: SkillEntity):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> SkillEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass