from app.repositories.base.category_repository_base import CategoryRepositoryBase
from app.configs.db.database import CategoryEntity
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.filter.category_filter import CategoryFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple

class CategoryRepositoryProvider(CategoryRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

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

    async def get_all(self, is_active: bool) -> list[CategoryEntity]:
        stmt: Final[Select[Tuple[CategoryEntity]]] = select(CategoryEntity).where(CategoryEntity.is_active == is_active)

        result: Final = await self.db.execute(stmt)
        all_categories: Final = result.scalars().all()
        return list(all_categories)

    async def get_all_filter(self, is_active: bool, filter: CategoryFilter) -> list[CategoryEntity]:
        stmt = select(CategoryEntity).where(CategoryEntity.is_active == is_active)

        stmt = filter.filter(stmt)

        result: Final = await self.db.execute(stmt)
        all_categories: Final = result.scalars().all()
        return list(all_categories)

    async def delete(self, category: CategoryEntity) -> None:
        await self.db.delete(category)
        await self.db.commit()

    async def get_by_id(self, id: int) -> CategoryEntity | None:
        if id is None or id <= 0:
            return None

        stmt = select(CategoryEntity).where(CategoryEntity.id == id)

        result: Final[Result[Tuple[CategoryEntity]]] = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save(self, category: CategoryEntity) -> CategoryEntity:
        await self.db.commit()
        await self.db.refresh(category)

        return category

    async def add(self, category: CategoryEntity) -> CategoryEntity:
        self.db.add(category)

        await self.db.commit()
        await self.db.refresh(category)

        return category