from app.repositories.base.favorite_posts_enterprise_repository_base import FavoritePostEnterpriseRepositoryBase
from app.configs.db.database import FavoritePostEnterpriseEntity, PostEnterpriseEntity
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from typing import Final

class FavoritePostUserRepositoryProvider(FavoritePostEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> FavoritePostEnterpriseEntity | None:
        stmt = select(FavoritePostEnterpriseEntity).where(
            and_(
                FavoritePostEnterpriseEntity.user_id == user_id,
                FavoritePostEnterpriseEntity.post_enterprise_id == post_enterprise_id
            )
        )

        result: Final = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_user_id_and_post_enterprise_id(self, user_id: int, post_enterprise_id: int) -> bool:
        stmt = select(func.count(FavoritePostEnterpriseEntity.id)).where(
            and_(
                FavoritePostEnterpriseEntity.user_id == user_id,
                FavoritePostEnterpriseEntity.post_enterprise_id == post_enterprise_id
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)
    
    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostEnterpriseEntity]:
        if user_id is None or user_id <= 0:
            return []

        stmt = (
            select(FavoritePostEnterpriseEntity)
            .options(
                joinedload(FavoritePostEnterpriseEntity.owner),   
                joinedload(FavoritePostEnterpriseEntity.posts)
            )
            .where(FavoritePostEnterpriseEntity.user_id == user_id)
            .order_by(FavoritePostEnterpriseEntity.created_at.desc())
        )

        result: Final = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostEnterpriseEntity]:
        if user_id is None or user_id <= 0:
            return []

        stmt = (
            select(PostEnterpriseEntity)
            .join(FavoritePostEnterpriseEntity, PostEnterpriseEntity.id == FavoritePostEnterpriseEntity.post_enterprise_id)
            .where(FavoritePostEnterpriseEntity.user_id == user_id)
            .order_by(FavoritePostEnterpriseEntity.created_at.desc())
        )

        result = await self.db.execute(stmt)
        posts: Final[list[PostEnterpriseEntity]] = list(result.scalars().all())

        return posts

    async def get_by_id(self, id: int) -> FavoritePostEnterpriseEntity | None:
        if id is None or id <= 0:
            return None
        
        result = await self.db.execute(
            select(FavoritePostEnterpriseEntity).where(FavoritePostEnterpriseEntity.id == id)
        )

        return result.scalars().first()

    async def add(self, favo: FavoritePostEnterpriseEntity) -> FavoritePostEnterpriseEntity:
        self.db.add(favo)
        await self.db.commit()
        await self.db.refresh(favo)

        return favo

    async def delete(self, favo: FavoritePostEnterpriseEntity):
        await self.db.delete(favo)
        await self.db.commit()