from abc import ABC, abstractmethod

from app.configs.db.database import RolesEntity


class RolesServiceBase(ABC):

    @abstractmethod
    async def get_by_title(self, title: str) -> RolesEntity | None:
        pass