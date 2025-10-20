from app.repositories.base.area_repository_base import AreaRepositoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import AreaEntity
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.area_filter import AreaFilter
from sqlalchemy import select, func
from typing import Final, List
from datetime import datetime

class AreaRepositoryProvider(
    AreaRepositoryBase,
    GenericRepository[
        AreaEntity,
        AreaFilter,
        int,
        AreaEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=AreaEntity)

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(AreaEntity.name)).where(
            AreaEntity.name.ilike(f"%{name}%")
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)