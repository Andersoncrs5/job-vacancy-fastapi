from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import FavoriteCommentPostUserEntity, CommentPostUserEntity
from app.repositories.base.favorite_comment_post_user_repository_base import FavoriteCommentPostUserRepositoryBase

import uuid

class FavoriteCommentPostUserRepositoryProvider(FavoriteCommentPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> FavoriteCommentPostUserEntity | None:
        stmt = select(FavoriteCommentPostUserEntity).where(
            and_(
                FavoriteCommentPostUserEntity.user_id == user_id,
                FavoriteCommentPostUserEntity.comment_user_id == comment_user_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        stmt = select(func.count(FavoriteCommentPostUserEntity.id)).where(
            and_(
                FavoriteCommentPostUserEntity.user_id == user_id,
                FavoriteCommentPostUserEntity.comment_user_id == comment_user_id,
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result)

    async def add(self, favor: FavoriteCommentPostUserEntity) -> FavoriteCommentPostUserEntity:
        favor.id = uuid.uuid4()

        self.db.add(favor)
        await self.db.commit()
        await self.db.refresh(favor)

        return favor

    async def delete(self, favor: FavoriteCommentPostUserEntity):
        await self.db.delete(favor)
        await self.db.commit()

    async def get_all(self, user_id: int | None, comment_user_id: int | None) -> list[FavoriteCommentPostUserEntity]:
        stmt = (
            select(FavoriteCommentPostUserEntity)
            .options(
                joinedload(FavoriteCommentPostUserEntity.comment)

                .joinedload(CommentPostUserEntity.user),

                joinedload(FavoriteCommentPostUserEntity.comment)

                .joinedload(CommentPostUserEntity.post),

                joinedload(FavoriteCommentPostUserEntity.user),
            )
        )

        if user_id is not None:
            stmt = stmt.where(FavoriteCommentPostUserEntity.user_id == user_id)

        if comment_user_id is not None:
            stmt = stmt.where(FavoriteCommentPostUserEntity.comment_user_id == comment_user_id)

        stmt = stmt.order_by(FavoriteCommentPostUserEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())