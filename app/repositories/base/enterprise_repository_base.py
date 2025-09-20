from abc import ABC, abstractmethod
from app.configs.db.database import EnterpriseEntity
from app.utils.filter.enterprise_filter import EnterpriseFilter

class EnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def add(self, enter: EnterpriseEntity) -> EnterpriseEntity:
        pass
    
    @abstractmethod
    async def get_all_filter(self, filter: EnterpriseFilter) -> list[EnterpriseEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> EnterpriseEntity | None:
        pass

    @abstractmethod
    async def save(self, enter: EnterpriseEntity) -> EnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, enter: EnterpriseEntity):
        pass