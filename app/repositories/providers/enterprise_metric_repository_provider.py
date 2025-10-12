from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import EnterpriseMetricEntity
from app.repositories.base.enterprise_metric_repository_base import EnterpriseMetricRepositoryBase


class EnterpriseMetricRepositoryProvider(EnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        stmt = select(EnterpriseMetricEntity).where(
            EnterpriseMetricEntity.enterprise_id == enterprise_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Enterprise metric not found")

        return metric

    async def exists_by_id(self, enterprise_id: int) -> bool:
        stmt = select(func.count(EnterpriseMetricEntity.enterprise_id)).where(
            EnterpriseMetricEntity.enterprise_id == enterprise_id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def delete(self, metric: EnterpriseMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def add(self, metric: EnterpriseMetricEntity) -> None:
        self.db.add(metric)
        await self.db.commit()

    async def save(self, metric: EnterpriseMetricEntity) -> EnterpriseMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric