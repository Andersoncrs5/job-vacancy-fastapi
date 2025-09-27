from app.repositories.base.my_skill_repository_base import MySkillRepositoryBase
from app.configs.db.database import MySkillEntity
from app.utils.filter.my_skill_filter import MySkillFilter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, func, and_ 
from typing import Final

class MySkillRepositoryProvider(MySkillRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> bool:
        stmt = select(func.count(MySkillEntity.user_id)).where(
            and_(
                MySkillEntity.user_id == user_id,
                MySkillEntity.skill_id == skill_id,
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_skill_id_and_user_id(self, skill_id: int, user_id: int) -> MySkillEntity | None:
        stmt = select(MySkillEntity).where(
            and_(
                MySkillEntity.user_id == user_id,
                MySkillEntity.skill_id == skill_id,
            )
        )

        result: Final = await self.db.execute(stmt)
        return result.scalars().first()

    async def delete(self, my: MySkillEntity):
        await self.db.delete(my)
        await self.db.commit()

    async def get_all(self, filter: MySkillFilter) -> list[MySkillEntity]: 
        stmt = filter.filter(select(MySkillEntity))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)

    async def save(self, my: MySkillEntity) -> MySkillEntity:
        my.updated_at = datetime.now()

        await self.db.commit()
        await self.db.refresh(my)

        return my

    async def add(self, my: MySkillEntity) -> MySkillEntity:
        self.db.add(my)
        await self.db.commit()
        await self.db.refresh(my)

        return my