from app.repositories.base.saved_search_repository_base import SavedSearchReposioryBase
from app.configs.db.database import SavedSearchEntity
from app.utils.filter.saved_search_filter import SavedSearchFilter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, func
from typing import List, Final

class SavedSearchReposioryProvider(SavedSearchReposioryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_id(self, id: int) -> bool :
        stmt = select(func.count(SavedSearchEntity.id)).where(
            SavedSearchEntity.id == id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_id(self, id: int) -> SavedSearchEntity | None:
        result = await self.db.execute(
            select(SavedSearchEntity).where(SavedSearchEntity.id == id)
        )

        return result.scalars().first()

    async def save(self, save: SavedSearchEntity) -> SavedSearchEntity:
        save.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(save)

        return save

    async def add(self, save: SavedSearchEntity) -> SavedSearchEntity:
        self.db.add(save)
        await self.db.commit()
        await self.db.refresh(save)

        return save

    async def delete(self, save: SavedSearchEntity):
        await self.db.delete(save)
        await self.db.commit()

    async def get_all(self, filter: SavedSearchFilter) -> List[SavedSearchEntity]:
        stmt = filter.filter(select(SavedSearchEntity))

        result = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)