from abc import ABC, abstractmethod

from app.configs.db.database import FollowerRelationshipEntity

class FollowRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, follower_id: int) -> list[FollowerRelationshipEntity] :
        pass

    @abstractmethod
    async def save(self, follow: FollowerRelationshipEntity) -> FollowerRelationshipEntity:
        pass

    @abstractmethod
    async def add(self, follow: FollowerRelationshipEntity) -> FollowerRelationshipEntity:
        pass

    @abstractmethod
    async def exists_by_follower_id_and_followed_id(self, follower_id: int, followed_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_follower_id_and_followed_id(self, follower_id: int, followed_id: int) -> FollowerRelationshipEntity | None:
        pass

    @abstractmethod
    async def delete(self, follow: FollowerRelationshipEntity):
        pass