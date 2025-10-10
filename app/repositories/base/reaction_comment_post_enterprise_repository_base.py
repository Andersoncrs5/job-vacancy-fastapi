from abc import abstractmethod, ABC

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum

import uuid

from app.utils.filter.reaction_comment_post_enterprise_filter import ReactionCommentPostEnterpriseFilter


class ReactionCommentPostEnterpriseRepositoryBase(ABC):
    @abstractmethod
    async def get_all(
            self,
            filter: ReactionCommentPostEnterpriseFilter
    ) -> list[ReactionCommentPostEnterpriseEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> ReactionCommentPostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def get_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> ReactionCommentPostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def save(self, react: ReactionCommentPostEnterpriseEntity) -> ReactionCommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, react: ReactionCommentPostEnterpriseEntity):
        pass

    @abstractmethod
    async def add(self, react: ReactionCommentPostEnterpriseEntity) -> ReactionCommentPostEnterpriseEntity:
        pass

    @abstractmethod
    async def exists_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> bool:
        pass