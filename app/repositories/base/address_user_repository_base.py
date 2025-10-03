from abc import ABC, abstractmethod
from app.configs.db.database import AddressUserEntity

class AddressUserRepositoryBase(ABC):

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
    async def save(self, address: AddressUserEntity) -> AddressUserEntity:
        pass
    
    @abstractmethod
    async def add(self, address: AddressUserEntity) -> AddressUserEntity:
        pass
    
