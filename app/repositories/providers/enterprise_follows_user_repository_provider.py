from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import EnterpriseFollowsUserEntity
from app.repositories.base.enterprise_follows_user_repository_base import EnterpriseFollowsUserRepositoryBase
from app.utils.filter.enterprise_follows_user_filter import EnterpriseFollowsUserFilter


class EnterpriseFollowsUserRepositoryProvider(EnterpriseFollowsUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, filter: EnterpriseFollowsUserFilter):
        stmt = filter.filter(select(EnterpriseFollowsUserEntity))

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def add(self, follow: EnterpriseFollowsUserEntity) -> EnterpriseFollowsUserEntity:
        self.db.add(follow)
        await self.db.commit()
        await self.db.refresh(follow)

        return follow

    async def save(self, follow: EnterpriseFollowsUserEntity) -> EnterpriseFollowsUserEntity:
        self.db.add(follow)
        await self.db.commit()
        await self.db.refresh(follow)

        return follow

    async def delete(self, follow: EnterpriseFollowsUserEntity):
        await self.db.delete(follow)
        await self.db.commit()

    async def get_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> EnterpriseFollowsUserEntity | None:
        stmt = select(EnterpriseFollowsUserEntity).where(
            and_(
                EnterpriseFollowsUserEntity.enterprise_id == enterprise_id,
                EnterpriseFollowsUserEntity.user_id == user_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_enterprise_id_and_user_id(
            self,
            enterprise_id: int,
            user_id: int
    ) -> bool:
        stmt = select(func.count(EnterpriseFollowsUserEntity.id)).where(
            and_(
                EnterpriseFollowsUserEntity.enterprise_id == enterprise_id,
                EnterpriseFollowsUserEntity.user_id == user_id,
            )
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)