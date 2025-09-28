from abc import ABC, abstractmethod
from app.configs.db.database import EmployeeEnterpriseEntity
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter
from app.schemas.employee_enterprise_schemas import CreateEmployeeEnterpriseDTO, UpdateEmployeeEnterpriseDTO

class EmployeeEnterpriseServiceBase(ABC):

    @abstractmethod
    async def get_all(self, filter: EmployeeEnterpriseFilter) -> list[EmployeeEnterpriseEntity]:
        pass

    @abstractmethod
    async def update(self, emp: EmployeeEnterpriseEntity, dto: UpdateEmployeeEnterpriseDTO) -> EmployeeEnterpriseEntity:
        pass

    @abstractmethod
    async def create(self, user_id: int, enterprise_id:int, dto: CreateEmployeeEnterpriseDTO) -> EmployeeEnterpriseEntity:
        pass

    @abstractmethod
    async def delete(self, emp: EmployeeEnterpriseEntity):
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        pass
