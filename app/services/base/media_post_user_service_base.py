
from abc import ABC, abstractmethod
from typing import List

from app.configs.db.database import MediaPostUserEntity
from app.schemas.media_post_user_schemas import CreateMediaPostUserDTO, UpdateMediaPostUserDTO
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter

class MediaPostUserServiceBase(ABC):

    @abstractmethod
    async def get_amount_by_post_id(self, post_id: int) -> int:
        pass

    @abstractmethod
    async def update(self, media: MediaPostUserEntity, dto: UpdateMediaPostUserDTO) -> MediaPostUserEntity:
        pass
    
    @abstractmethod
    async def create(self, post_id: int, dto: CreateMediaPostUserDTO) -> MediaPostUserEntity:
        pass
    
    @abstractmethod
    async def get_all_filter(self, filter: MediaPostUserFilter) -> List[MediaPostUserFilter]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> MediaPostUserEntity | None:
        pass

    @abstractmethod
    async def delete(self, media: MediaPostUserEntity):
        pass