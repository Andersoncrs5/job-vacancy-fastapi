from abc import ABC, abstractmethod
from app.configs.db.database import FavoritePostEnterpriseEntity, PostEnterpriseEntity

class FavoritePostEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> FavoritePostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def get_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> FavoritePostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        pass

    @abstractmethod
    async def add(self, favo: FavoritePostEnterpriseEntity) -> FavoritePostEnterpriseEntity:
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostEnterpriseEntity]:
        pass
    
    @abstractmethod
    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostEnterpriseEntity]:
        pass

    @abstractmethod
    async def delete(self, favo: FavoritePostEnterpriseEntity):
        pass