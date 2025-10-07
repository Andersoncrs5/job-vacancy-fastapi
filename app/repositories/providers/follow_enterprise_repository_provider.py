from typing import Final

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import FollowerRelationshipEnterpriseEntity
from app.repositories.base.follow_enterprise_repository_base import FollowEnterpriseRepositoryBase


class FollowEnterpriseRepositoryProvider(FollowEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, follow: FollowerRelationshipEnterpriseEntity) -> FollowerRelationshipEnterpriseEntity:
        self.db.add(follow)
        await self.db.commit()
        await self.db.refresh(follow)

        return follow

    async def delete(self, follow: FollowerRelationshipEnterpriseEntity):
        await self.db.delete(follow)
        await self.db.commit()

    async def get_by_user_id_and_enterprise_id(self, user_id: int,
                                               enterprise_id: int) -> FollowerRelationshipEnterpriseEntity | None:
        stmt = select(FollowerRelationshipEnterpriseEntity).where(
            and_(
                FollowerRelationshipEnterpriseEntity.user_id == user_id,
                FollowerRelationshipEnterpriseEntity.enterprise_id == enterprise_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_enterprise_id(self, user_id: int, enterprise_id: int) -> bool:
        stmt = select(func.count(FollowerRelationshipEnterpriseEntity.id)).where(
            and_(
                FollowerRelationshipEnterpriseEntity.user_id == user_id,
                FollowerRelationshipEnterpriseEntity.enterprise_id == enterprise_id,
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all_filtered(
            self, user_id: int | None = None, enterprise_id: int | None = None
    ) -> list[FollowerRelationshipEnterpriseEntity]:
        stmt = select(FollowerRelationshipEnterpriseEntity).options(
            joinedload(FollowerRelationshipEnterpriseEntity.followed_enterprise),
            joinedload(FollowerRelationshipEnterpriseEntity.follower),
        )

        if user_id is not None:
            stmt = stmt.where(FollowerRelationshipEnterpriseEntity.user_id == user_id)
        if enterprise_id is not None:
            stmt = stmt.where(FollowerRelationshipEnterpriseEntity.enterprise_id == enterprise_id)

        stmt = stmt.order_by(FollowerRelationshipEnterpriseEntity.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
