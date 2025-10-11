from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import UserMetricEntity
from app.repositories.base.user_metric_repository_base import UserMetricRepositoryBase


class UserMetricRepositoryProvider(UserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> UserMetricEntity | None:
        stmt = select(UserMetricEntity).where(
            UserMetricEntity.user_id == user_id
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_id(self, user_id: int) -> bool:
        stmt = select(func.count(UserMetricEntity.user_id)).where(
            UserMetricEntity.user_id == user_id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def delete(self, metric: UserMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def add(self, metric: UserMetricEntity) -> UserMetricEntity:
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)

        return metric