from abc import ABC, abstractmethod

from app.configs.db.database import FavoriteCommentPostUserEntity


class FavoriteCommentPostUserServiceBase(ABC):

    @abstractmethod
    async def create(self, user_id: int, comment_user_id: int) -> FavoriteCommentPostUserEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> FavoriteCommentPostUserEntity | None:
        pass

    @abstractmethod
    async def get_all(
            self, user_id: int | None, comment_user_id: int | None
    ) -> list[FavoriteCommentPostUserEntity]:
        pass

    @abstractmethod
    async def delete(self, favor: FavoriteCommentPostUserEntity):
        pass