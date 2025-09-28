from abc import ABC, abstractmethod
from app.configs.db.database import EmployeeEnterpriseEntity
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter

class EmployeeEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool :
        pass
    
    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool :
        pass
    
    @abstractmethod
    async def get_all(self, filter: EmployeeEnterpriseFilter) -> list[EmployeeEnterpriseEntity]:
        pass
    
    @abstractmethod
    async def save(self, emp: EmployeeEnterpriseEntity) -> EmployeeEnterpriseEntity:
        pass

    @abstractmethod
    async def add(self, emp: EmployeeEnterpriseEntity) -> EmployeeEnterpriseEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, emp: EmployeeEnterpriseEntity):
        pass