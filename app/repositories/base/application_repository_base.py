from abc import ABC, abstractmethod

from app.configs.db.database import ApplicationEntity
from app.utils.filter.applications_filter import ApplicationFilter


class ApplicationRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: ApplicationFilter) -> list[ApplicationEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> ApplicationEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def save(self, app: ApplicationEntity) -> ApplicationEntity:
        pass

    @abstractmethod
    async def delete(self, app: ApplicationEntity):
        pass

    @abstractmethod
    async def add(self, app: ApplicationEntity) -> ApplicationEntity:
        pass