from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import CommentPostEnterpriseEntity
from app.repositories.base.comment_post_enterprise_repository_base import CommentPostEnterpriseRepositoryBase
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseRepositoryProvider(CommentPostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> CommentPostEnterpriseEntity | None:
        stmt = (
            select(CommentPostEnterpriseEntity)
            .options(
                joinedload(CommentPostEnterpriseEntity.user),
                joinedload(CommentPostEnterpriseEntity.post),
            )
            .where(
                CommentPostEnterpriseEntity.id == id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def delete(self, comment: CommentPostEnterpriseEntity):
        await self.db.delete(comment)
        await self.db.commit()

    async def get_all(self, filter: CommentPostEnterpriseFilter) -> list[CommentPostEnterpriseEntity]:
        stmt = filter.filter(
            select(CommentPostEnterpriseEntity)
            .options(
                joinedload(CommentPostEnterpriseEntity.user),
                joinedload(CommentPostEnterpriseEntity.post),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def add(self, comment: CommentPostEnterpriseEntity) -> CommentPostEnterpriseEntity:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def save(self, comment: CommentPostEnterpriseEntity) -> CommentPostEnterpriseEntity:
        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def exists_by_id(self, id: int) -> bool:
        stmt = select(func.count(CommentPostEnterpriseEntity.id)).where(
            CommentPostEnterpriseEntity.id == id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)