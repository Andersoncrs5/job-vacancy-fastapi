import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import PostEnterpriseMetricEntity
from app.repositories.base.post_enterprise_metric_repository_base import PostEnterpriseMetricRepositoryBase

logger = structlog.get_logger()


class PostEnterpriseMetricRepositoryProvider(PostEnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, metric: PostEnterpriseMetricEntity) -> PostEnterpriseMetricEntity:
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def delete(self, metric: PostEnterpriseMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        stmt = select(PostEnterpriseMetricEntity).where(
            PostEnterpriseMetricEntity.post_id == post_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric Post Enterprise not found")

        return metric