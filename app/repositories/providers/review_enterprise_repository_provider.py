from typing import Final, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import ReviewEnterprise
from app.repositories.base.review_enterprise_repository_base import ReviewEnterpriseRepositoryBase
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter


class ReviewEnterpriseRepositoryProvider(ReviewEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    

    async def get_all(self, filter: ReviewEnterpriseFilter) -> List[ReviewEnterprise]:
        stmt = filter.filter(select(ReviewEnterprise))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)