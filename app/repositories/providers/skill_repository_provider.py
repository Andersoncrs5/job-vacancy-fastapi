from app.repositories.base.skill_repository_base import SkillRepositoryBase
from app.configs.db.database import SkillEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Final

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.skill_filter import SkillFilter
from typing import List
from datetime import datetime

class SkillRepositoryProvider(
    SkillRepositoryBase,
    GenericRepository[
        SkillEntity,
        SkillFilter,
        int,
        SkillEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=SkillEntity)

    async def exists_by_name(self, name: str) -> bool:
        result: Final[int | None] = await self.db.scalar(
            select(func.count(SkillEntity.id)).where(SkillEntity.name.ilike(f"%{name}%"))
        )

        if result is None:
            return False

        return result > 0
