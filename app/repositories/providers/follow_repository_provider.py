from typing import Final

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import FollowerRelationshipEntity
from app.repositories.base.follow_repository_base import FollowRepositoryBase


class FollowRepositoryProvider(FollowRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, follower_id: int) -> list[FollowerRelationshipEntity]:
        stmt = (
            select(FollowerRelationshipEntity)
            .options(
                joinedload(FollowerRelationshipEntity.follower),
                joinedload(FollowerRelationshipEntity.followed)
            )
            .where(
                FollowerRelationshipEntity.follower_id == follower_id
            )
            .order_by(FollowerRelationshipEntity.created_at.desc())
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def save(self, follow: FollowerRelationshipEntity) -> FollowerRelationshipEntity:
        await self.db.commit()
        await self.db.refresh(follow)

        return follow

    async def add(self, follow: FollowerRelationshipEntity) -> FollowerRelationshipEntity:
        self.db.add(follow)
        await self.db.commit()
        await self.db.refresh(follow)

        return follow

    async def delete(self, follow: FollowerRelationshipEntity):
        await self.db.delete(follow)
        await self.db.commit()

    async def exists_by_follower_id_and_followed_id(self, follower_id: int, followed_id: int) -> bool:
        stmt = select(func.count(FollowerRelationshipEntity.id)).where(
            and_(
                FollowerRelationshipEntity.follower_id == follower_id,
                FollowerRelationshipEntity.followed_id == followed_id,
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_follower_id_and_followed_id(
            self, follower_id: int,followed_id: int
        ) -> FollowerRelationshipEntity | None:
        stmt = select(FollowerRelationshipEntity).where(
            and_(
                FollowerRelationshipEntity.follower_id == follower_id,
                FollowerRelationshipEntity.followed_id == followed_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()