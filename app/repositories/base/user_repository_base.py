from abc import ABC, abstractmethod
from app.configs.db.database import UserEntity
from app.utils.filter.user_filter import UserFilter

class UserRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_name(self, name: str) -> (UserEntity | None):
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> (UserEntity | None):
        pass