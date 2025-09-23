from abc import ABC, abstractmethod
from app.configs.db.database import CurriculumEntity

class CurriculumRepositoryBase(ABC):

    @abstractmethod
    async def save(self, curri: CurriculumEntity) -> CurriculumEntity:
        pass
    
    @abstractmethod
    async def add(self, curri: CurriculumEntity) -> CurriculumEntity:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, curri: CurriculumEntity):
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> CurriculumEntity | None:
        pass

    