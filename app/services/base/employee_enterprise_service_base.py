from abc import ABC, abstractmethod
from app.configs.db.database import EmployeeEnterpriseEntity

class EmployeeEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        pass
