from datetime import datetime
from typing import Final, List
from sqlalchemy import select, func, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import ReviewEnterprise
from app.repositories.base.review_enterprise_repository_base import ReviewEnterpriseRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter


class ReviewEnterpriseRepositoryProvider(
    ReviewEnterpriseRepositoryBase,
    GenericRepository[
        ReviewEnterprise,
        ReviewEnterpriseFilter,
        int,
        ReviewEnterprise,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=ReviewEnterprise)

    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(ReviewEnterprise.user_id)).where(
            ReviewEnterprise.user_id == user_id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)