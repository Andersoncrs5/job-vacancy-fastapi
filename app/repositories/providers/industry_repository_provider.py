from app.repositories.base.industry_repository_base import IndustryRepositoryBase
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import IndustryEntity

class IndustryRepositoryProvider(IndustryRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(IndustryEntity.id)).where(IndustryEntity.name.ilike(f"%{name}%"))

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def delete(self, industry: IndustryEntity):
        await self.db.delete(industry)
        await self.db.commit()

    async def save(self, industry: IndustryEntity) -> IndustryEntity:
        await self.db.commit()
        await self.db.refresh(industry)

        return industry

    async def get_by_id(self, id: int) -> IndustryEntity | None:
        stmt = select(IndustryEntity).where(IndustryEntity.id == id)

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def add(self, industry: IndustryEntity) -> IndustryEntity:
        self.db.add(industry)
        await self.db.commit()
        await self.db.refresh(industry)

        return industry
