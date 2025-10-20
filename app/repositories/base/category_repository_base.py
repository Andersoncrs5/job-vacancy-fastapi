from abc import ABC, abstractmethod
from app.configs.db.database import CategoryEntity

class CategoryRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass