from app.repositories.base.user_repository_base import UserRepositoryBase
from app.configs.db.database import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.user_filter import UserFilter
from sqlalchemy import select, func
from typing import Final

class UserRepositoryProvider(
    UserRepositoryBase,
    GenericRepository[
        UserEntity,
        UserFilter,
        int,
        UserEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=UserEntity)

    async def get_by_email(self, email: str) -> (UserEntity | None):
        stmt: Final = select(UserEntity).where(UserEntity.email == email)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(func.count(UserEntity.id)).where(UserEntity.name == name)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(func.count(UserEntity.id)).where(UserEntity.email == email)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0