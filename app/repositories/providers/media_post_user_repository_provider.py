from app.repositories.base.media_post_user_repository_base import MediaPostUserRepositoryBase
from app.configs.db.database import MediaPostUserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Result, Select
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from typing import List, Final
from datetime import datetime

class MediaPostUserRepositoryProvider(MediaPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_filter(self, filter: MediaPostUserFilter) -> List[MediaPostUserFilter]:
        stmt = select(MediaPostUserFilter)

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