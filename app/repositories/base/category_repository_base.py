from abc import ABC, abstractmethod
from app.configs.db.database import CategoryEntity

class CategoryRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> CategoryEntity | None:
        pass

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def add(self, category: CategoryEntity) -> CategoryEntity:
        pass

    @abstractmethod
    async def delete(self, category: CategoryEntity) -> None:
        pass

    @abstractmethod
    async def save(self, category: CategoryEntity) -> CategoryEntity:
        pass

    @abstractmethod
    async def get_all(self, is_active: bool) -> list[CategoryEntity]:
        pass
