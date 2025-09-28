from app.repositories.base.employee_enterprise_repository_base import EmployeeEnterpriseRepositoryBase
from app.configs.db.database import EmployeeEnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Result
from datetime import datetime
from typing import Final
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter

class EmployeeEnterpriseRepositoryProvider(EmployeeEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_user_id(self, user_id: int) -> bool :
        stmt = select(func.count(EmployeeEnterpriseEntity.id)).where(
            EmployeeEnterpriseEntity.user_id == user_id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def exists_by_id(self, id: int) -> bool :
        stmt = select(func.count(EmployeeEnterpriseEntity.id)).where(
            EmployeeEnterpriseEntity.id == id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all(self, filter: EmployeeEnterpriseFilter) -> list[EmployeeEnterpriseEntity]:
        stmt = select(EmployeeEnterpriseEntity)

        stmt = filter.filter(stmt)

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)

    async def save(self, emp: EmployeeEnterpriseEntity) -> EmployeeEnterpriseEntity:
        emp.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(emp)

        return emp

    async def add(self, emp: EmployeeEnterpriseEntity) -> EmployeeEnterpriseEntity:
        self.db.add(emp)
        await self.db.commit()
        await self.db.refresh(emp)

        return emp

    async def get_by_id(self, id: int) -> EmployeeEnterpriseEntity | None:
        if id <= 0:
            raise ValueError("Id is null or less than 0")

        stmt = select(EmployeeEnterpriseEntity).where(EmployeeEnterpriseEntity.id == id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def delete(self, emp: EmployeeEnterpriseEntity):
        await self.db.delete(emp)
        await self.db.commit()