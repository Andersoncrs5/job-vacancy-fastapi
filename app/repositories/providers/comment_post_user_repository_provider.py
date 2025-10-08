from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import CommentPostUserEntity
from app.repositories.base.comment_post_user_repository_base import CommentPostUserRepositoryBase
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserRepositoryProvider(CommentPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> CommentPostUserEntity | None:
        stmt = select(CommentPostUserEntity).where(
            CommentPostUserEntity.id == id
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def delete(self, comment: CommentPostUserEntity):
        await self.db.delete(comment)
        await self.db.commit()

    async def get_all(self, filter: CommentPostUserFilter) -> list[CommentPostUserEntity]:
        stmt = filter.filter(
            select(CommentPostUserEntity)
            .options(
                joinedload(CommentPostUserEntity.user),
                joinedload(CommentPostUserEntity.post),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def add(self, comment: CommentPostUserEntity) -> CommentPostUserEntity:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def save(self, comment: CommentPostUserEntity) -> CommentPostUserEntity:
        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def exists_by_id(self, id: int) -> bool:
        stmt = select(func.count(CommentPostUserEntity.id)).where(
            CommentPostUserEntity.id == id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)