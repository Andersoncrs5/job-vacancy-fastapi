from abc import ABC, abstractmethod
from app.configs.db.database import EnterpriseEntity
from app.utils.filter.enterprise_filter import EnterpriseFilter

class EnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> EnterpriseEntity | None:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass
