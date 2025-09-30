from app.repositories.base.area_repository_base import AreaRepositoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import AreaEntity
from app.utils.filter.area_filter import AreaFilter
from sqlalchemy import select, func
from typing import Final, List
from datetime import datetime

class AreaRepositoryProvider(AreaRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, area: AreaEntity) -> AreaEntity:
        area.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(area)

        return area

    async def add(self, area: AreaEntity) -> AreaEntity:
        self.db.add(area)
        await self.db.commit()
        await self.db.refresh(area)

        return area

    async def delete(self, area: AreaEntity):
        await self.db.delete(area)
        await self.db.commit()

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(AreaEntity.name)).where(
            AreaEntity.name.ilike(f"%{name}%")
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_id(self, id: int) -> AreaEntity | None:
        stmt = select(AreaEntity).where(AreaEntity.id == id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_id(self, id: int) -> bool :
        stmt = select(func.count(AreaEntity.id)).where(
            AreaEntity.id == id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all(self, filter: AreaFilter) -> List[AreaEntity]:
        stmt = filter.filter(select(AreaEntity))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)