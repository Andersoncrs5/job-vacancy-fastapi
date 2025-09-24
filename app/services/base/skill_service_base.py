from abc import ABC , abstractmethod 
from uuid import UUID
from typing import Final
from app.utils.filter.skill_filter import SkillFilter
from app.configs.db.database import SkillEntity
from typing import List
from datetime import datetime
from app.schemas.skill_schemas import SkillOUT, CreateSkillDTO, UpdateSkillDTO

class SkillServiceBase(ABC):

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
    async def get_by_id(self, id: UUID) -> SkillEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: UUID) -> bool:
        pass