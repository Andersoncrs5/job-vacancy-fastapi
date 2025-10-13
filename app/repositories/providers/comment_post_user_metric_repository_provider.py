from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import CommentPostUserMetricEntity
from app.repositories.base.comment_post_user_metric_repository_base import CommentPostUserMetricRepositoryBase


class CommentPostUserMetricRepositoryProvider(CommentPostUserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, metric: CommentPostUserMetricEntity) -> CommentPostUserMetricEntity:
        self.db.add(metric)

        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def delete(self, metric: CommentPostUserMetricEntity) -> None:
        await self.db.delete(metric)
        await self.db.commit()

    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        stmt = select(CommentPostUserMetricEntity).where(
            CommentPostUserMetricEntity.comment_id == comment_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric Comment Post User not found")

        return metric