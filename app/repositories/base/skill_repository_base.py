from abc import ABC, abstractmethod
from app.configs.db.database import SkillEntity
from app.utils.filter.skill_filter import SkillFilter
from typing import List

class SkillRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass
