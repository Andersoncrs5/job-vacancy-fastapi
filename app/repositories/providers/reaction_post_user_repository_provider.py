from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import ReactionPostUserEntity
from app.repositories.base.reaction_post_user_repository_base import ReactionPostUserRepositoryBase


class ReactionPostUserRepositoryProvider(ReactionPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int | None, post_user_id: int | None) -> list[ReactionPostUserEntity]:
        stmt = (
            select(ReactionPostUserEntity).options(
                joinedload(ReactionPostUserEntity.post),
                joinedload(ReactionPostUserEntity.user),
            )
        )

        if user_id is not None:
            stmt = stmt.where(ReactionPostUserEntity.user_id == user_id)

        if post_user_id is not None:
            stmt = stmt.where(ReactionPostUserEntity.post_user_id == post_user_id)

        stmt = stmt.order_by(ReactionPostUserEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, reaction: ReactionPostUserEntity):
        await self.db.delete(reaction)
        await self.db.commit()

    async def add(self, reaction: ReactionPostUserEntity) -> ReactionPostUserEntity:
        self.db.add(reaction)
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def save(self, reaction: ReactionPostUserEntity) -> ReactionPostUserEntity:
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def exists_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> bool:
        stmt = (
            select(func.count(ReactionPostUserEntity.id)).where(
                and_(
                    ReactionPostUserEntity.post_user_id == post_user_id,
                    ReactionPostUserEntity.user_id == user_id,
                )
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_user_id_and_post_user_id(self, user_id: int, post_user_id: int) -> ReactionPostUserEntity | None:
        stmt = (
            select(ReactionPostUserEntity).where(
                and_(
                    ReactionPostUserEntity.post_user_id == post_user_id,
                    ReactionPostUserEntity.user_id == user_id,
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()