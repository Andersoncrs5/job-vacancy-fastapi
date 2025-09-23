
from abc import ABC, abstractmethod

from app.configs.db.database import MediaPostUserEntity


class MediaPostUserServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> MediaPostUserEntity | None:
        pass

    @abstractmethod
    async def delete(self, id: int):
        pass