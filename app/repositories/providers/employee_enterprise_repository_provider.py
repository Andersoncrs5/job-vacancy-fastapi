from app.repositories.base.employee_enterprise_repository_base import EmployeeEnterpriseRepositoryBase
from app.configs.db.database import EmployeeEnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Result
from datetime import datetime
from typing import Final

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.employee_enterprise_filter import EmployeeEnterpriseFilter

class EmployeeEnterpriseRepositoryProvider(
    EmployeeEnterpriseRepositoryBase,
    GenericRepository[
        EmployeeEnterpriseEntity,
        EmployeeEnterpriseFilter,
        int,
        EmployeeEnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=EmployeeEnterpriseEntity)

    async def exists_by_user_id(self, user_id: int) -> bool :
        stmt = select(func.count(EmployeeEnterpriseEntity.id)).where(
            EmployeeEnterpriseEntity.user_id == user_id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)
