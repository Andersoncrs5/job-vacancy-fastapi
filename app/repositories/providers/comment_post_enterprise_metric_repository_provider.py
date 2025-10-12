from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import CommentPostEnterpriseMetricEntity
from app.repositories.base.comment_post_enterprise_metric_repository_base import \
    CommentPostEnterpriseMetricRepositoryBase


class CommentPostEnterpriseMetricRepositoryProvider(CommentPostEnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, metric: CommentPostEnterpriseMetricEntity) -> CommentPostEnterpriseMetricEntity:
        self.db.add(metric)

        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def delete(self, metric: CommentPostEnterpriseMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        stmt = select(CommentPostEnterpriseMetricEntity).where(
            CommentPostEnterpriseMetricEntity.comment_id == comment_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric Post User not found")

        return metric