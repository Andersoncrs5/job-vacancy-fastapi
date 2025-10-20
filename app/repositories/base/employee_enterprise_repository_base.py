from abc import ABC, abstractmethod
from app.configs.db.database import EmployeeEnterpriseEntity
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter

class EmployeeEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool :
        pass