from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import ReactionPostEnterpriseEntity
from app.repositories.base.reaction_post_enterprise_base import ReactionPostEnterpriseRepositoryBase


class ReactionPostEnterpriseRepositoryProvider(ReactionPostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int | None, post_enterprise_id: int | None) -> list[ReactionPostEnterpriseEntity]:
        stmt = (
            select(ReactionPostEnterpriseEntity).options(
                joinedload(ReactionPostEnterpriseEntity.post_enterprise),
                joinedload(ReactionPostEnterpriseEntity.user),
            )
        )

        if user_id is not None:
            stmt = stmt.where(ReactionPostEnterpriseEntity.user_id == user_id)

        if post_enterprise_id is not None:
            stmt = stmt.where(ReactionPostEnterpriseEntity.post_enterprise_id == post_enterprise_id)

        stmt = stmt.order_by(ReactionPostEnterpriseEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, reaction: ReactionPostEnterpriseEntity):
        await self.db.delete(reaction)
        await self.db.commit()

    async def add(self, reaction: ReactionPostEnterpriseEntity) -> ReactionPostEnterpriseEntity:
        self.db.add(reaction)
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def save(self, reaction: ReactionPostEnterpriseEntity) -> ReactionPostEnterpriseEntity:
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        stmt = (
            select(func.count(ReactionPostEnterpriseEntity.id)).where(
                and_(
                    ReactionPostEnterpriseEntity.post_enterprise_id == post_enterprise_id,
                    ReactionPostEnterpriseEntity.user_id == user_id,
                )
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> ReactionPostEnterpriseEntity | None:
        stmt = (
            select(ReactionPostEnterpriseEntity).where(
                and_(
                    ReactionPostEnterpriseEntity.post_enterprise_id == post_enterprise_id,
                    ReactionPostEnterpriseEntity.user_id == user_id,
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()