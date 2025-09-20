from abc import ABC, abstractmethod
from app.configs.db.database import EnterpriseEntity

class EnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> EnterpriseEntity | None:
        pass

    