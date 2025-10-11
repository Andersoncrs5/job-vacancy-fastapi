from abc import ABC, abstractmethod

from app.configs.db.database import UserMetricEntity


class UserMetricRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserMetricEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, metric: UserMetricEntity) -> None:
        pass

    @abstractmethod
    async def add(self, metric: UserMetricEntity) -> UserMetricEntity:
        pass