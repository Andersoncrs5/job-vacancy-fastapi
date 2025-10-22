from typing import Any, Coroutine

from sqlalchemy import select, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import RolesEntity
from app.repositories.base.roles_repository_base import RolesRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.roles_filter import RolesFilter


class RolesRepositoryProvider(
    RolesRepositoryBase,
    GenericRepository[
        RolesEntity,
        RolesFilter,
        int,
        RolesEntity,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=RolesEntity)

    async def exists_by_title(self, title: str) -> bool:
        stmt = select(func.count(RolesEntity.id)).where(
            RolesEntity.title == title
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(func.count(RolesEntity.id)).where(
            RolesEntity.slug == slug
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_slug(self, slug: str) -> RolesEntity | None:
        stmt = select(RolesEntity).where(RolesEntity.slug == slug)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def get_by_title(self, title: str) -> RolesEntity | None:
        stmt = select(RolesEntity).where(RolesEntity.title == title)

        result = await self.db.execute(stmt)

        return result.scalars().first()