from abc import ABC, abstractmethod
from app.configs.db.database import CurriculumEntity

class CurriculumRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> CurriculumEntity | None:
        pass

    