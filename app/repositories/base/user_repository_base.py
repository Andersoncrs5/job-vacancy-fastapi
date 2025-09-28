from abc import ABC, abstractmethod
from app.configs.db.database import UserEntity
from app.utils.filter.user_filter import UserFilter

class UserRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: UserFilter) -> list[UserEntity]:
        pass
    
    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def add(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def delete(self, user: UserEntity) -> None:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> (UserEntity | None):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> (UserEntity | None):
        pass

