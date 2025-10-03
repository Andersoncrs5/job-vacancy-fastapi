from abc import ABC, abstractmethod
from app.configs.db.database import AddressUserEntity
from app.schemas.address_user_schemas import CreateAddressUserDTO, UpdateAddressUserDTO

class AddressUserServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> AddressUserEntity | None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> AddressUserEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, address: AddressUserEntity):
        pass
    
    @abstractmethod
    async def create(self, user_id: int, dto: CreateAddressUserDTO) -> AddressUserEntity:
        pass
    
    @abstractmethod
    async def update(self, address: AddressUserEntity, dto: UpdateAddressUserDTO) -> AddressUserEntity:
        pass