from app.repositories.base.post_user_repository_base import *
from app.configs.db.database import PostUserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.filter.post_user_filter import PostUserFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple

class PostUserRepositoryProvider(PostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_id(self, id: int) -> bool:
        stmt = select(func.count(PostUserEntity.id)).where(PostUserEntity.id == id)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def get_all_filter(self, filter: PostUserFilter) -> list[PostUserEntity]:
        stmt = select(PostUserEntity)

        stmt = filter.filter(stmt)

        result: Final = await self.db.execute(stmt)
        all_categories: Final = result.scalars().all()
        return list(all_categories)

    async def get_by_id(self, id: int) -> (PostUserEntity | None):
        if id is None or id <= 0:
            return None

        stmt: Final = select(PostUserEntity).where(PostUserEntity.id == id)

        result: Final[Result[Tuple[PostUserEntity]]] = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save(self, post: PostUserEntity) -> PostUserEntity:
        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def create(self, post: PostUserEntity) -> PostUserEntity:
        self.db.add(post)

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete(self, post: PostUserEntity):
        await self.db.delete(post)
        await self.db.commit()