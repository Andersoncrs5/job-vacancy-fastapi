from app.repositories.base.enterprise_repository_base import EnterpriseRepositoryBase
from app.configs.db.database import EnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.utils.filter.enterprise_filter import EnterpriseFilter
from typing import Final

class EnterpriseRepositoryProvider(EnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

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

    async def get_all_filter(self, filter: EnterpriseFilter) -> list[EnterpriseEntity]:
        stmt = filter.filter(select(EnterpriseEntity))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)

    async def add(self, enter: EnterpriseEntity) -> EnterpriseEntity:
        self.db.add(enter)
        await self.db.commit()
        await self.db.refresh(enter)

        return enter

    async def get_by_id(self, id: int) -> EnterpriseEntity | None:
        result = await self.db.execute(
            select(EnterpriseEntity).where(EnterpriseEntity.id == id)
        )
        return result.scalars().first()

    async def delete(self, enter: EnterpriseEntity):
        await self.db.delete(enter)
        await self.db.commit()

    async def save(self, enter: EnterpriseEntity) -> EnterpriseEntity:
        await self.db.commit()
        await self.db.refresh(enter)

        return enter