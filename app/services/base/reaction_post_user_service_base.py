from abc import ABC, abstractmethod

from app.configs.db.database import ReactionPostUserEntity


class ReactionPostUserServiceBase(ABC):

    @abstractmethod
    async def get_all(self, user_id: int | None, post_user_id: int | None) -> list[ReactionPostUserEntity]:
        pass

    @abstractmethod
    async def create(self, user_id: int, post_user_id: int) -> ReactionPostUserEntity:
        pass

    @abstractmethod
    async def delete(self, reaction: ReactionPostUserEntity):
        pass

    @abstractmethod
    async def toggle_reaction_type(self, reaction: ReactionPostUserEntity) -> ReactionPostUserEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> ReactionPostUserEntity | None:
        pass
