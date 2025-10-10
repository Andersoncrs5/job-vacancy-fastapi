from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import ReactionCommentPostEnterpriseEntity
from app.repositories.base.reaction_comment_post_enterprise_repository_base import \
    ReactionCommentPostEnterpriseRepositoryBase
from app.utils.filter.reaction_comment_post_enterprise_filter import ReactionCommentPostEnterpriseFilter


class ReactionCommentPostEnterpriseRepositoryProvider(ReactionCommentPostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
            self,
            filter: ReactionCommentPostEnterpriseFilter
    ) -> list[ReactionCommentPostEnterpriseEntity]:
        stmt = filter.filter(select(ReactionCommentPostEnterpriseEntity))

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def add(self, react: ReactionCommentPostEnterpriseEntity) -> ReactionCommentPostEnterpriseEntity:
        self.db.add(react)
        await self.db.commit()
        await self.db.refresh(react)

        return react

    async def save(self, react: ReactionCommentPostEnterpriseEntity) -> ReactionCommentPostEnterpriseEntity:
        await self.db.commit()
        await self.db.refresh(react)

        return react

    async def delete(self, react: ReactionCommentPostEnterpriseEntity):
        await self.db.delete(react)
        await self.db.commit()

    async def get_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> ReactionCommentPostEnterpriseEntity | None:
        stmt = select(ReactionCommentPostEnterpriseEntity).where(
            and_(
                    ReactionCommentPostEnterpriseEntity.user_id == user_id,
                    ReactionCommentPostEnterpriseEntity.comment_enterprise_id == comment_enterprise_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_comment_enterprise_id(
            self,
            user_id: int,
            comment_enterprise_id: int
    ) -> bool:
        stmt = select(func.count(ReactionCommentPostEnterpriseEntity.id)).where(
            and_(
                ReactionCommentPostEnterpriseEntity.user_id == user_id,
                ReactionCommentPostEnterpriseEntity.comment_enterprise_id == comment_enterprise_id,
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result)

    async def get_by_id(self, id: UUID) -> ReactionCommentPostEnterpriseEntity | None:
        stmt = select(ReactionCommentPostEnterpriseEntity).where(
            ReactionCommentPostEnterpriseEntity.id == id
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()