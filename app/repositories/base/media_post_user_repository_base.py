from abc import ABC, abstractmethod
from app.configs.db.database import MediaPostUserEntity
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from typing import List

class MediaPostUserRepositoryBase(ABC):

    @abstractmethod
    async def get_all_filter(self, filter: MediaPostUserFilter) -> List[MediaPostUserFilter]:
        pass

    @abstractmethod
    async def add(self, media: MediaPostUserEntity) -> MediaPostUserEntity:
        pass

    @abstractmethod
    async def save(self, media: MediaPostUserEntity) -> MediaPostUserEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> MediaPostUserEntity | None:
        pass

    @abstractmethod
    async def delete(self, media: MediaPostUserEntity):
        pass
