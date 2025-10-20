from app.repositories.base.category_repository_base import CategoryRepositoryBase
from app.configs.db.database import CategoryEntity
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.category_filter import CategoryFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple

class CategoryRepositoryProvider(
    CategoryRepositoryBase,
    GenericRepository[
        CategoryEntity,
        CategoryFilter,
        int,
        CategoryEntity,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=CategoryEntity)

    async def exists_by_name(self, name: str) -> bool:
        stmt: Final = select(func.count(CategoryEntity.id)).where(CategoryEntity.name.ilike(f"%{name}%"))

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def exists_by_slug(self, slug: str) -> bool:
        stmt: Final = select(func.count(CategoryEntity.id)).where(CategoryEntity.slug.ilike(f"%{slug}%"))  

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0