from datetime import datetime
from typing import Final, List
from sqlalchemy import select, func, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import ReviewEnterprise
from app.repositories.base.review_enterprise_repository_base import ReviewEnterpriseRepositoryBase
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter


class ReviewEnterpriseRepositoryProvider(ReviewEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(ReviewEnterprise.user_id)).where(
            ReviewEnterprise.user_id == user_id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def exists_by_id(self, id: int) -> bool :
        stmt = select(func.count(ReviewEnterprise.id)).where(
            ReviewEnterprise.id == id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_id(self, id: int) -> ReviewEnterprise | None:
        if id is None or id <= 0:
            raise ValueError("Id is required")

        stmt = select(ReviewEnterprise).where(ReviewEnterprise.id == id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def delete(self, view: ReviewEnterprise):
        await self.db.delete(view)
        await self.db.commit()

    async def add(self, view: ReviewEnterprise) -> ReviewEnterprise:
        self.db.add(view)
        await self.db.commit()
        await self.db.refresh(view)

        return view

    async def save(self, view: ReviewEnterprise) -> ReviewEnterprise:
        view.updated_at = datetime.now()

        await self.db.commit()
        await self.db.refresh(view)

        return view

    async def get_all(self, filter: ReviewEnterpriseFilter) -> List[ReviewEnterprise]:
        stmt = filter.filter(select(ReviewEnterprise))

        result: Final = await self.db.execute(stmt)
        all: Final = result.scalars().all()
        return list(all)