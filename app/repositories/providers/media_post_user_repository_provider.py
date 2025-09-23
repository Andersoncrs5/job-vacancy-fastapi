from app.repositories.base.media_post_user_repository_base import MediaPostUserRepositoryBase
from app.configs.db.database import MediaPostUserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from typing import List, Final
from datetime import datetime

class MediaPostUserRepositoryProvider(MediaPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_amount_by_post_id(self, post_id: int) -> int:
        stmt = select(func.count(MediaPostUserEntity.id)).where(MediaPostUserEntity.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() or 0

    async def get_all_filter(self, filter: MediaPostUserFilter) -> List[MediaPostUserEntity]:
        stmt = select(MediaPostUserEntity)

        stmt = filter.filter(stmt)

        result = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)

    async def get_by_id(self, id: int) -> MediaPostUserEntity | None:
        if id <= 0:
            raise ValueError("id is required")

        stmt = await self.db.execute(
            select(MediaPostUserEntity).where(MediaPostUserEntity.id == id)
        )

        return stmt.scalar_one_or_none()

    async def add(self, media: MediaPostUserEntity) -> MediaPostUserEntity:
        self.db.add(media)
        await self.db.commit()
        await self.db.refresh(media)

        return media

    async def save(self, media: MediaPostUserEntity) -> MediaPostUserEntity:
        media.updated_at = datetime.now()
        
        await self.db.commit()
        await self.db.refresh(media)

        return media

    async def delete(self, media: MediaPostUserEntity):
        await self.db.delete(media)
        await self.db.commit()