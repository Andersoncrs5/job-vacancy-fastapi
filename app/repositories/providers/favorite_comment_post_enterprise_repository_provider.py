import uuid

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import FavoriteCommentPostEnterpriseEntity, CommentPostEnterpriseEntity
from app.repositories.base.favorite_comment_post_enterprise_repository_base import \
    FavoriteCommentPostEnterpriseRepositoryBase


class FavoriteCommentPostEnterpriseRepositoryProvider(FavoriteCommentPostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> FavoriteCommentPostEnterpriseEntity | None:
        stmt = select(FavoriteCommentPostEnterpriseEntity).where(
            and_(
                FavoriteCommentPostEnterpriseEntity.user_id == user_id,
                FavoriteCommentPostEnterpriseEntity.comment_enterprise_id == comment_enterprise_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_comment_enterprise_id(
            self, user_id: int, comment_enterprise_id: int
    ) -> bool:
        stmt = select(func.count(FavoriteCommentPostEnterpriseEntity.id)).where(
            and_(
                FavoriteCommentPostEnterpriseEntity.user_id == user_id,
                FavoriteCommentPostEnterpriseEntity.comment_enterprise_id == comment_enterprise_id,
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result)

    async def add(self, favor: FavoriteCommentPostEnterpriseEntity) -> FavoriteCommentPostEnterpriseEntity:
        favor.id = uuid.uuid4()

        self.db.add(favor)
        await self.db.commit()
        await self.db.refresh(favor)

        return favor

    async def delete(self, favor: FavoriteCommentPostEnterpriseEntity):
        await self.db.delete(favor)
        await self.db.commit()

    async def get_all(self, user_id: int | None, comment_enterprise_id: int | None) -> list[
        FavoriteCommentPostEnterpriseEntity]:
        stmt = (
            select(FavoriteCommentPostEnterpriseEntity)
            .options(
                joinedload(FavoriteCommentPostEnterpriseEntity.comment)

                .joinedload(CommentPostEnterpriseEntity.user),

                joinedload(FavoriteCommentPostEnterpriseEntity.comment)

                .joinedload(CommentPostEnterpriseEntity.post),

                joinedload(FavoriteCommentPostEnterpriseEntity.user),
            )
        )

        if user_id is not None:
            stmt = stmt.where(FavoriteCommentPostEnterpriseEntity.user_id == user_id)

        if comment_enterprise_id is not None:
            stmt = stmt.where(FavoriteCommentPostEnterpriseEntity.comment_enterprise_id == comment_enterprise_id)

        stmt = stmt.order_by(FavoriteCommentPostEnterpriseEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())