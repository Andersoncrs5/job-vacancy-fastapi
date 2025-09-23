from app.repositories.base.curriculum_repository_base import CurriculumRepositoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.configs.db.database import CurriculumEntity
from typing import Final
from datetime import datetime

class CurriculumRepositoryProvider(CurriculumRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, curri: CurriculumEntity) -> CurriculumEntity:
        curri.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(curri)

        return curri

    async def add(self, curri: CurriculumEntity) -> CurriculumEntity:
        self.db.add(curri)
        await self.db.commit()
        await self.db.refresh(curri)

        return curri

    async def delete(self, curri: CurriculumEntity):
        await self.db.delete(curri)
        await self.db.commit()

    async def get_by_user_id(self, user_id: int) -> CurriculumEntity | None:
        result: Final = await self.db.execute(
            select(CurriculumEntity).where(CurriculumEntity.user_id == user_id)
        )

        return result.scalars().first()
        
    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(CurriculumEntity.id)).where(CurriculumEntity.user_id == user_id)
        
        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0
