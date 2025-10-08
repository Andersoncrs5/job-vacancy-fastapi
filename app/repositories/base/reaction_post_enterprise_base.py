from abc import ABC, abstractmethod

from app.configs.db.database import ReactionPostEnterpriseEntity

class ReactionPostEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, user_id: int | None, post_enterprise_id: int | None) -> list[ReactionPostEnterpriseEntity]:
        pass

    @abstractmethod
    async def add(self, reaction: ReactionPostEnterpriseEntity) -> ReactionPostEnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, reaction: ReactionPostEnterpriseEntity):
        pass

    @abstractmethod
    async def save(self, reaction: ReactionPostEnterpriseEntity) -> ReactionPostEnterpriseEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> ReactionPostEnterpriseEntity | None:
        pass