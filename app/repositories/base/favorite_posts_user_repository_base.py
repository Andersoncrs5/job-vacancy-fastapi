from abc import ABC, abstractmethod
from app.configs.db.database import FavoritePostUserEntity, PostUserEntity

class FavoritePostUserRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> FavoritePostUserEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id_post_id(self, user_id, post_id) -> bool:
        pass

    @abstractmethod
    async def add(self, favo: FavoritePostUserEntity) -> FavoritePostUserEntity:
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostUserEntity]:
        pass
    
    @abstractmethod
    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostUserEntity]:
        pass

    @abstractmethod
    async def delete(self, favo: FavoritePostUserEntity):
        pass