from typing import Final
from sqlalchemy.orm import joinedload
from app.configs.db.database import VacancySkillEntity
from app.repositories.base.vacancy_skill_repository_base import VacancySkillRepositoryBase
from sqlalchemy import and_, select, func, Result, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.vacancy_skill_filter import VacancySkillFilter


class VacancySkillRepositoryProvider(
    VacancySkillRepositoryBase,
    GenericRepository[
        VacancySkillEntity,
        VacancySkillFilter,
        int,
        VacancySkillEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=VacancySkillEntity)

    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        stmt = select(func.count(VacancySkillEntity.id)).where(
            and_(
                VacancySkillEntity.vacancy_id == vacancy_id,
                VacancySkillEntity.skill_id == skill_id,
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all_by_vacancy_id(self, vacancy_id: int) -> list[VacancySkillEntity]:
        stmt = (
            select(VacancySkillEntity)
            .where(VacancySkillEntity.vacancy_id == vacancy_id)
            .options(joinedload(VacancySkillEntity.skill))
        )
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())