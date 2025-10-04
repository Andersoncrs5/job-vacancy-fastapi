from abc import ABC, abstractmethod
from app.configs.db.database import AddressEnterpriseEntity

class AddressEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_enterprise_id(self, enterprise_id: int) -> AddressEnterpriseEntity | None:
        pass

    @abstractmethod
    async def exists_by_enterprise_id(self, enterprise_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, address: AddressEnterpriseEntity):
        pass
    
    @abstractmethod
    async def save(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        pass
    
    @abstractmethod
    async def add(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        pass
    
