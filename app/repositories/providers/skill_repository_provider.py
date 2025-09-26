from app.repositories.base.skill_repository_base import SkillRepositoryBase
from app.configs.db.database import SkillEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Final
from app.utils.filter.skill_filter import SkillFilter
from typing import List
from datetime import datetime

class SkillRepositoryProvider(SkillRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, skill: SkillEntity) -> SkillEntity:
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)

        return skill

    async def save(self, skill: SkillEntity) -> SkillEntity:
        skill.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(skill)

        return skill

    async def get_all(self, filter: SkillFilter) -> List[SkillEntity]:
        stmt = filter.filter(select(SkillEntity))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)

    async def delete(self, skill: SkillEntity):
        await self.db.delete(skill)
        await self.db.commit()

    async def get_by_id(self, id: int) -> (SkillEntity | None):
        result = await self.db.execute(
            select(SkillEntity).where(SkillEntity.id == id)
        )

        return result.scalars().first()

    async def exists_by_name(self, name: str) -> bool:
        result: Final[int | None] = await self.db.scalar(
            select(func.count(SkillEntity.id)).where(SkillEntity.name.ilike(f"%{name}%"))
        )

        if result is None:
            return False

        return result > 0

    async def exists_by_id(self, id: int) -> bool:
        result: Final[int | None] = await self.db.scalar(
            select(func.count(SkillEntity.id)).where(SkillEntity.id == id)
        )

        if result is None:
            return False

        return result > 0