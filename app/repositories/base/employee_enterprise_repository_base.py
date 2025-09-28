from abc import ABC, abstractmethod
from app.configs.db.database import EmployeeEnterpriseEntity

class EmployeeEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, emp: EmployeeEnterpriseEntity):
        pass