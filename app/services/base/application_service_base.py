from abc import ABC, abstractmethod
from typing import TypeVar

from app.configs.db.database import ApplicationEntity
from app.schemas.application_schemas import UpdateApplicationDTO
from app.utils.filter.applications_filter import ApplicationFilter


class ApplicationServiceBase(ABC):

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def update(self, app: ApplicationEntity, dto: UpdateApplicationDTO) -> ApplicationEntity:
        pass

    @abstractmethod
    async def exists_by_application(self, user_id: int, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, vacancy_id: int, user_id: int) -> ApplicationEntity:
        pass