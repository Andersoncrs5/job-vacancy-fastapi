from abc import ABC, abstractmethod
from app.configs.db.database import AddressEnterpriseEntity
from app.schemas.address_enterprise_schemas import CreateAddressEnterpriseDTO, UpdateAddressEnterpriseDTO

class AddressEnterpriseServiceBase(ABC):

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
    async def toggle_is_public(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        pass

    @abstractmethod
    async def create(self, enterprise_id: int, dto: CreateAddressEnterpriseDTO) -> AddressEnterpriseEntity:
        pass
    
    @abstractmethod
    async def update(self, address: AddressEnterpriseEntity, dto: UpdateAddressEnterpriseDTO) -> AddressEnterpriseEntity:
        pass