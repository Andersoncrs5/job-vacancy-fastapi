from abc import ABC, abstractmethod
from app.configs.db.database import EnterpriseEntity, UserEntity, IndustryEntity
from app.schemas.enterprise_schemas import CreateEnterpriseDTO, UpdateEnterpriseDTO
from app.utils.filter.enterprise_filter import EnterpriseFilter

class EnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_all_filter(self, filter: EnterpriseFilter) -> list[EnterpriseEntity]:
        pass

    @abstractmethod
    async def update(self, enter: EnterpriseEntity, dto: UpdateEnterpriseDTO) -> EnterpriseEntity:
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def delete(self, enter: EnterpriseEntity):
        pass

    @abstractmethod
    async def create(self, industry: IndustryEntity, user: UserEntity ,dto: CreateEnterpriseDTO) -> EnterpriseEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> EnterpriseEntity | None:
        pass

