from app.repositories.base.media_post_user_repository_base import MediaPostUserRepositoryBase
from app.configs.db.database import MediaPostUserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from typing import List, Final
from datetime import datetime

class MediaPostUserRepositoryProvider(
    MediaPostUserRepositoryBase,
    GenericRepository[
        MediaPostUserEntity,
        MediaPostUserFilter,
        int,
        MediaPostUserEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=MediaPostUserEntity)

    async def get_amount_by_post_id(self, post_id: int) -> int:
        stmt = select(func.count(MediaPostUserEntity.id)).where(MediaPostUserEntity.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() or 0