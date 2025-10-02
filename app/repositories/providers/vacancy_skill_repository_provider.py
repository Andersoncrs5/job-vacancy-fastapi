from typing import Final
from sqlalchemy.orm import joinedload
from app.configs.db.database import VacancySkillEntity
from app.repositories.base.vacancy_skill_repository_base import VacancySkillRepositoryBase
from sqlalchemy import and_, select, func, Result, Select
from sqlalchemy.ext.asyncio import AsyncSession

class VacancySkillRepositoryProvider(VacancySkillRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        self.db.add(vs)
        await self.db.commit()
        await self.db.refresh(vs)

        return vs

    async def save(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        await self.db.commit()
        await self.db.refresh(vs)

        return vs

    async def delete(self, vs: VacancySkillEntity) -> None:
        await self.db.delete(vs)
        await self.db.commit()

    async def get_by_id(self, id: int) -> VacancySkillEntity | None:
        result = await self.db.execute(
            select(VacancySkillEntity).where(VacancySkillEntity.id == id)
        )

        return result.scalars().first()

    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        stmt = select(func.count(VacancySkillEntity.id)).where(
            and_(
                VacancySkillEntity.vacancy_id == vacancy_id,
                VacancySkillEntity.skill_id == skill_id,
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all(self, vacancy_id: int) -> list[VacancySkillEntity]:
        stmt = (
            select(VacancySkillEntity)
            .where(VacancySkillEntity.vacancy_id == vacancy_id)
            .options(joinedload(VacancySkillEntity.skill))
        )
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
