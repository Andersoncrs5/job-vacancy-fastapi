from app.repositories.base.favorite_posts_user_repository_base import FavoritePostUserRepositoryBase
from app.configs.db.database import FavoritePostUserEntity, PostUserEntity
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from typing import Final

class FavoritePostUserRepositoryProvider(FavoritePostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_by_user_id(self, user_id: int) -> list[FavoritePostUserEntity]:
        if user_id is None or user_id <= 0:
            return []

        stmt = (
            select(FavoritePostUserEntity)
            .options(
                joinedload(FavoritePostUserEntity.owner),   
                joinedload(FavoritePostUserEntity.post_user)
            )
            .where(FavoritePostUserEntity.user_id == user_id)
            .order_by(FavoritePostUserEntity.created_at.desc())
        )

        result: Final = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all_by_user_id_just_post(self, user_id: int) -> list[PostUserEntity]:
        if user_id is None or user_id <= 0:
            return []

        stmt = (
            select(PostUserEntity)
            .join(FavoritePostUserEntity, PostUserEntity.id == FavoritePostUserEntity.post_user_id)
            .where(FavoritePostUserEntity.user_id == user_id)
            .order_by(FavoritePostUserEntity.created_at.desc())
        )

        result = await self.db.execute(stmt)
        posts: Final[list[PostUserEntity]] = list(result.scalars().all())

        return posts

    async def exists_by_user_id_post_id(self, user_id: int, post_id: int) -> bool:
        stmt = select(func.count(FavoritePostUserEntity.id)).where(
            and_(
                FavoritePostUserEntity.user_id == user_id,
                FavoritePostUserEntity.post_user_id == post_id
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_id(self, id: int) -> FavoritePostUserEntity | None:
        if id is None or id <= 0:
            return None
        
        result = await self.db.execute(
            select(FavoritePostUserEntity).where(FavoritePostUserEntity.id == id)
        )

        return result.scalars().first()

    async def add(self, favo: FavoritePostUserEntity) -> FavoritePostUserEntity:
        self.db.add(favo)
        await self.db.commit()
        await self.db.refresh(favo)

        return favo

    async def delete(self, favo: FavoritePostUserEntity):
        await self.db.delete(favo)
        await self.db.commit()