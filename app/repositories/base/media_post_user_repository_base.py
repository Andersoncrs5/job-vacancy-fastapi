from abc import ABC, abstractmethod
from app.configs.db.database import MediaPostUserEntity
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from typing import List

class MediaPostUserRepositoryBase(ABC):

    @abstractmethod
    async def get_amount_by_post_id(self, post_id: int) -> int:
        pass