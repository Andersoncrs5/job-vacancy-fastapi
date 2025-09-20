from abc import ABC, abstractmethod
from app.configs.db.database import IndustryEntity

class IndustryRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> IndustryEntity | None:
        pass

    @abstractmethod
    async def delete(self, industry: IndustryEntity) -> None:
        pass

    @abstractmethod
    async def save(self, industry: IndustryEntity) -> IndustryEntity:
        pass

    @abstractmethod
    async def add(self, industry: IndustryEntity) -> IndustryEntity:
        pass

    