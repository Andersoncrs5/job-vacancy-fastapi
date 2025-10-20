from abc import ABC, abstractmethod
from app.configs.db.database import IndustryEntity
from app.utils.filter.industry_filter import IndustryFilter

class IndustryRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass
