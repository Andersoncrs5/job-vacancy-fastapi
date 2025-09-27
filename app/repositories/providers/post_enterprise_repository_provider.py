from app.repositories.base.post_user_repository_base import *
from app.configs.db.database import PostEnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple
from app.repositories.base.post_enterprise_repository_base import PostEnterpriseRepositoryBase

class PostEnterpriseRepositoryProvider(PostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_id(self, id: int) -> bool:
        stmt = select(func.count(PostEnterpriseEntity.id)).where(PostEnterpriseEntity.id == id)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def get_all(self, filter: PostEnterpriseFilter) -> list[PostEnterpriseEntity]:
        stmt = select(PostEnterpriseEntity)

        stmt = filter.filter(stmt)

        result: Final = await self.db.execute(stmt)
        all_categories: Final = result.scalars().all()
        return list(all_categories)

    async def get_by_id(self, id: int) -> (PostEnterpriseEntity | None):
        if id is None or id <= 0:
            return None

        stmt: Final = select(PostEnterpriseEntity).where(PostEnterpriseEntity.id == id)

        result: Final[Result[Tuple[PostEnterpriseEntity]]] = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save(self, post: PostEnterpriseEntity) -> PostEnterpriseEntity:
        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def create(self, post: PostEnterpriseEntity) -> PostEnterpriseEntity:
        self.db.add(post)

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete(self, post: PostEnterpriseEntity):
        await self.db.delete(post)
        await self.db.commit()