from app.services.base.employee_enterprise_service_base import EmployeeEnterpriseServiceBase
from app.repositories.providers.employee_enterprise_repository_provider import EmployeeEnterpriseRepositoryProvider
from app.configs.db.database import EmployeeEnterpriseEntity
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter
from app.schemas.employee_enterprise_schemas import CreateEmployeeEnterpriseDTO, UpdateEmployeeEnterpriseDTO

class EmployeeEnterpriseServiceProvider(EmployeeEnterpriseServiceBase):
    def __init__(self, repository: EmployeeEnterpriseRepositoryProvider):
        self.repository = repository    

    async def get_all(self, filter: EmployeeEnterpriseFilter) -> list[EmployeeEnterpriseEntity]:
        return await self.repository.get_all(filter)

    async def update(self, emp: EmployeeEnterpriseEntity, dto: UpdateEmployeeEnterpriseDTO) -> EmployeeEnterpriseEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(emp, field, value)

        return await self.repository.save(emp)

    async def create(self, user_id: int, enterprise_id:int, dto: CreateEmployeeEnterpriseDTO) -> EmployeeEnterpriseEntity:
        employee = dto.to_entity()

        employee.user_id = user_id
        employee.enterprise_id = enterprise_id

        return await self.repository.add(employee)

    async def delete(self, emp: EmployeeEnterpriseEntity):
        await self.repository.delete(emp)

    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        return await self.repository.get_by_id(id)

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)