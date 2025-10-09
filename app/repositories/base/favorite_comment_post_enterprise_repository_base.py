from abc import ABC, abstractmethod

from app.configs.db.database import FavoriteCommentPostEnterpriseEntity


class FavoriteCommentPostEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> FavoriteCommentPostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> bool:
        pass

    @abstractmethod
    async def add(self, favor: FavoriteCommentPostEnterpriseEntity) -> FavoriteCommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def save(self, favor: FavoriteCommentPostEnterpriseEntity) -> FavoriteCommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, favor: FavoriteCommentPostEnterpriseEntity):
        pass

    @abstractmethod
    async def get_all(self, user_id: int | None, comment_enterprise_id: int | None) -> list[FavoriteCommentPostEnterpriseEntity]:
        pass