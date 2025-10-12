from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import PostUserMetricEntity
from app.repositories.base.post_user_metric_repository_base import PostUserMetricRepositoryBase


class PostUserMetricRepositoryProvider(PostUserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, metric: PostUserMetricEntity) -> PostUserMetricEntity:
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def delete(self, metric: PostUserMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        stmt = select(PostUserMetricEntity).where(
            PostUserMetricEntity.post_id == post_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric Post User not found")

        return metric