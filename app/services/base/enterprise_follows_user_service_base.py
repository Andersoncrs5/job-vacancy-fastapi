from abc import ABC, abstractmethod

from app.configs.db.database import EnterpriseFollowsUserEntity
from app.utils.filter.enterprise_follows_user_filter import EnterpriseFollowsUserFilter


class EnterpriseFollowsUserServiceBase(ABC):

    @abstractmethod
    async def get_all(self, filter: EnterpriseFollowsUserFilter):
        pass

    @abstractmethod
    async def create(self, enterprise_id: int, user_id: int) -> EnterpriseFollowsUserEntity:
        pass

    @abstractmethod
    async def delete(self, follow: EnterpriseFollowsUserEntity):
        pass

    @abstractmethod
    async def get_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> EnterpriseFollowsUserEntity | None:
        pass

    @abstractmethod
    async def exists_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> bool:
        pass