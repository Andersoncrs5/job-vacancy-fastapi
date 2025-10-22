from abc import ABC, abstractmethod

from app.configs.db.database import RolesEntity


class RolesRepositoryBase(ABC):
    @abstractmethod
    async def get_by_slug(self, slug: str) -> RolesEntity | None:
        pass

    @abstractmethod
    async def exists_by_title(self, title: str) -> bool:
        pass
