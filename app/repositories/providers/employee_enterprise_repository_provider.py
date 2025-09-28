from app.repositories.base.employee_enterprise_repository_base import EmployeeEnterpriseRepositoryBase
from app.configs.db.database import EmployeeEnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Result

class EmployeeEnterpriseRepositoryProvider(EmployeeEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        if id <= 0:
            raise ValueError("Id is null or less than 0")

        stmt = select(EmployeeEnterpriseEntity).where(EmployeeEnterpriseEntity.id == id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def delete(self, emp: EmployeeEnterpriseEntity):
        await self.db.delete(emp)
        await self.db.commit()