import datetime
from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import ApplicationEntity
from app.repositories.base.application_repository_base import ApplicationRepositoryBase
from app.utils.filter.applications_filter import ApplicationFilter
from sqlalchemy import select, func

class ApplicationRepositoryProvider(ApplicationRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, filter: ApplicationFilter) -> list[ApplicationEntity]:
        result: Final = await self.db.execute(
            filter.filter(select(ApplicationEntity))
        )

        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> ApplicationEntity | None:
        result = await self.db.execute(
            select(ApplicationEntity).where(ApplicationEntity.id == id)
        )

        return result.scalars().first()

    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(ApplicationEntity.id)).where(
            ApplicationEntity.user_id == user_id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def save(self, app: ApplicationEntity) -> ApplicationEntity:
        app.updated_at = datetime.datetime.now()
        await self.db.commit()
        await self.db.refresh(app)

        return app

    async def add(self, app: ApplicationEntity) -> ApplicationEntity:
        self.db.add(app)
        await self.db.commit()
        await self.db.refresh(app)

        return app

    async def delete(self, app: ApplicationEntity):
        await self.db.delete(app)
        await self.db.commit()