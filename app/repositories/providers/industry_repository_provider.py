from app.repositories.base.industry_repository_base import IndustryRepositoryBase
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.industry_filter import IndustryFilter
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import IndustryEntity

class IndustryRepositoryProvider(
    IndustryRepositoryBase,
    GenericRepository[
        IndustryEntity,
        IndustryFilter,
        int,
        IndustryEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=IndustryEntity)

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(IndustryEntity.id)).where(IndustryEntity.name.ilike(f"%{name}%"))

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0
