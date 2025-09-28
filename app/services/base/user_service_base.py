from abc import ABC, abstractmethod
from app.schemas.user_schemas import CreateUserDTO, UpdateUserDTO
from app.configs.db.database import UserEntity
from app.utils.filter.user_filter import UserFilter

class UserServiceBase(ABC):
    
    @abstractmethod
    async def get_all(self, filter: UserFilter) -> list[UserEntity]:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    async def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        pass

    @abstractmethod
    async def create(self, dto: CreateUserDTO) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> (UserEntity | None):
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> (UserEntity | None):
        pass

    @abstractmethod
    async def delete(self, user: UserEntity):
        pass