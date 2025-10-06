from abc import ABC, abstractmethod

from app.configs.db.database import FollowerRelationshipEntity


class FollowServiceBase(ABC):

    @abstractmethod
    async def delete(self, follow: FollowerRelationshipEntity):
        pass

    @abstractmethod
    async def create(self,  user_id: int, followed_id: int) -> FollowerRelationshipEntity:
        pass

    @abstractmethod
    async def get_by_follower_id_and_followed_id(self, user_id: int,
                                                 followed_id: int) -> FollowerRelationshipEntity | None:
        pass

    @abstractmethod
    async def exists_by_follower_id_and_followed_id(self, user_id: int, followed_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all(self, user_id: int) -> list[FollowerRelationshipEntity]:
        pass
