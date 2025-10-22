from abc import ABC, abstractmethod

from app.configs.db.database import UserRolesEntity


class MyRolesRepositoryBase(ABC):
    @abstractmethod
    async def get_by_user_id_and_role_id(self, user_id: int, role_id: int) -> (UserRolesEntity | None):
        pass

    @abstractmethod
    async def exists_by_user_id_and_role_id(self, user_id: int, role_id: int) -> bool:
        pass
