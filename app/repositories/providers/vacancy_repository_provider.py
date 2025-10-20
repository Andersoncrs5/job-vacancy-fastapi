from app.repositories.base.vacancy_repository_base import VacancyRepositoryBase
from sqlalchemy import select, func, Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import VacancyEntity
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import Final, Tuple, List

class VacancyRepositoryProvider(
    VacancyRepositoryBase,
    GenericRepository[
        VacancyEntity,
        VacancyFilter,
        int,
        VacancyEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=VacancyEntity)