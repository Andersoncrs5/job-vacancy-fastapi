from datetime import datetime
from typing import Final

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import NotificationEnterpriseEntity
from app.repositories.base.notification_enterprise_repository_base import NotificationEnterpriseRepositoryBase
from app.utils.filter.notification_enterprise_filter import NotificationEnterpriseFilter


class NotificationEnterpriseRepositoryProvider(NotificationEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, _id: int) -> NotificationEnterpriseEntity | None:
        stmt = select(NotificationEnterpriseEntity).where(
            NotificationEnterpriseEntity.id == _id
        )

        data = await self.db.execute(stmt)

        return data.scalars().first()

    async def get_all(self, _filter: NotificationEnterpriseFilter) -> list[NotificationEnterpriseEntity]:
        stmt = _filter.filter(select(NotificationEnterpriseEntity))

        data = await self.db.execute(stmt)

        return list(data.scalars().all())

    async def save(self, noti: NotificationEnterpriseEntity) -> NotificationEnterpriseEntity:
        noti.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def add(self, noti: NotificationEnterpriseEntity) -> NotificationEnterpriseEntity:
        self.db.add(noti)
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def delete(self, noti: NotificationEnterpriseEntity):
        await self.db.delete(noti)
        await self.db.commit()

    async def exists_by_id(self, _id: int) -> bool:
        stmt = select(func.count(NotificationEnterpriseEntity.id)).where(
            NotificationEnterpriseEntity.id == _id
        )

        data: Final[int | None] = await self.db.scalar(stmt)

        return bool(data and data > 0)