from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import ReactionCommentPostUserEntity

import uuid

from app.configs.db.enums import ReactionTypeEnum
from app.repositories.base.reaction_comment_post_user_repository_base import ReactionCommentPostUserRepositoryBase


class ReactionCommentPostUserRepositoryProvider(ReactionCommentPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
            self, user_id: int | None,
            comment_user_id: int | None,
            reaction_type: ReactionTypeEnum | None
    ) -> list[ReactionCommentPostUserEntity]:
        stmt = (
            select(ReactionCommentPostUserEntity)
        )

        if user_id is not None:
            stmt = stmt.where(ReactionCommentPostUserEntity.user_id == user_id)

        if comment_user_id is not None:
            stmt = stmt.where(ReactionCommentPostUserEntity.comment_user_id == comment_user_id)

        if reaction_type is not None:
            stmt = stmt.where(ReactionCommentPostUserEntity.reaction_type == reaction_type)

        stmt = stmt.order_by(ReactionCommentPostUserEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> ReactionCommentPostUserEntity | None:
        stmt = select(ReactionCommentPostUserEntity).where(
            and_(
                ReactionCommentPostUserEntity.user_id == user_id,
                ReactionCommentPostUserEntity.comment_user_id == comment_user_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_comment_user_id(
            self, user_id: int, comment_user_id: int
    ) -> bool:
        stmt = select(func.count(ReactionCommentPostUserEntity.id)).where(
            and_(
                ReactionCommentPostUserEntity.user_id == user_id,
                ReactionCommentPostUserEntity.comment_user_id == comment_user_id,
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result)

    async def delete(self, react: ReactionCommentPostUserEntity):
        await self.db.delete(react)
        await self.db.commit()

    async def add(self, react: ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        self.db.add(react)
        await self.db.commit()
        await self.db.refresh(react)

        return react

    async def get_by_id(self, id: uuid.UUID) -> ReactionCommentPostUserEntity | None:
        stmt = select(ReactionCommentPostUserEntity).where(
            ReactionCommentPostUserEntity.id == id
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def save(self, react: ReactionCommentPostUserEntity) -> ReactionCommentPostUserEntity:
        await self.db.commit()
        await self.db.refresh(react)

        return react