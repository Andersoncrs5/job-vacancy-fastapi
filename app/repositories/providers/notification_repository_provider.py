from datetime import datetime
from typing import Final

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import NotificationEntity
from app.repositories.base.notification_repository_base import NotificationRepositoryBase
from app.utils.filter.notification_filter import NotificationFilter


class NotificationRepositoryProvider(NotificationRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, _id: int) -> NotificationEntity | None:
        stmt = select(NotificationEntity).where(
            NotificationEntity.id == _id
        )

        data = await self.db.execute(stmt)

        return data.scalars().first()

    async def get_all(self, _filter: NotificationFilter) -> list[NotificationEntity]:
        stmt = _filter.filter(select(NotificationEntity))

        data = await self.db.execute(stmt)

        return list(data.scalars().all())

    async def save(self, noti: NotificationEntity) -> NotificationEntity:
        noti.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def add(self, noti: NotificationEntity) -> NotificationEntity:
        self.db.add(noti)
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def delete(self, noti: NotificationEntity):
        await self.db.delete(noti)
        await self.db.commit()

    async def exists_by_id(self, _id: int) -> bool:
        stmt = select(func.count(NotificationEntity.id)).where(
            NotificationEntity.id == _id
        )

        data: Final[int | None] = await self.db.scalar(stmt)

        return bool(data and data > 0)