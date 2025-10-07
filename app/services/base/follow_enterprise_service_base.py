from abc import ABC, abstractmethod

from app.configs.db.database import FollowerRelationshipEnterpriseEntity


class FollowEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_all_filtered(
            self, user_id: int | None = None, enterprise_id: int | None = None
    ) -> list[FollowerRelationshipEnterpriseEntity]:
        pass

    @abstractmethod
    async def create(self, user_id: int, enterprise_id: int) -> FollowerRelationshipEnterpriseEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_enterprise_id(self, user_id: int, enterprise_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id_and_enterprise_id(
            self, user_id: int, enterprise_id: int
    ) -> FollowerRelationshipEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, follow: FollowerRelationshipEnterpriseEntity):
        pass