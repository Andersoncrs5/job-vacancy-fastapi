from app.repositories.base.enterprise_repository_base import EnterpriseRepositoryBase
from app.configs.db.database import EnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.enterprise_filter import EnterpriseFilter
from typing import Final

class EnterpriseRepositoryProvider(
    EnterpriseRepositoryBase,
    GenericRepository[
        EnterpriseEntity,
        EnterpriseFilter,
        int,
        EnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=EnterpriseEntity)

    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(EnterpriseEntity.id)).where(EnterpriseEntity.user_id == user_id)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(EnterpriseEntity.id)).where(EnterpriseEntity.name.ilike(f"%{name}%"))

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def get_by_user_id(self, user_id: int) -> EnterpriseEntity | None:
        result = await self.db.execute(
            select(EnterpriseEntity).where(EnterpriseEntity.user_id == user_id)
        )
        return result.scalars().first()