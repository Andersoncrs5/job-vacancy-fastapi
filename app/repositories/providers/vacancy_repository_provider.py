from app.repositories.base.vacancy_repository_base import VacancyRepositoryBase
from sqlalchemy import select, func, Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import Final, Tuple, List

class VacancyRepositoryProvider(VacancyRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_id(self, id: int) -> bool :
        result: Final[int | None] = await self.db.scalar(
            select(func.count(VacancyEntity.id)).where(VacancyEntity.id == id)
        )

        return bool(result and result > 0)

    async def get_by_id(self, id: int) -> VacancyEntity | None:
        result = await self.db.execute(
            select(VacancyEntity).where(VacancyEntity.id == id)
        )

        return result.scalars().first()

    async def add(self, vacancy: VacancyEntity) -> VacancyEntity:
        self.db.add(vacancy)
        await self.db.commit()
        await self.db.refresh(vacancy)

        return vacancy

    async def save(self, vacancy: VacancyEntity) -> VacancyEntity:
        await self.db.commit()
        await self.db.refresh(vacancy)

        return vacancy

    async def get_all(self, filter: VacancyFilter) -> List[VacancyEntity]:
        result = await self.db.execute(
            filter.filter(select(VacancyEntity))
        )

        return list(result.scalars().all())