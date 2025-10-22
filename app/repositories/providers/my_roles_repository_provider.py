from typing import Final

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import MyRolesEntity
from app.repositories.base.my_roles_repository_base import MyRolesRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.my_role_filter import MyRolesFilter


class MyRolesRepositoryProvider(
    MyRolesRepositoryBase,
    GenericRepository[
        MyRolesEntity,
        MyRolesFilter,
        int,
        MyRolesEntity,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=MyRolesEntity)

    async def exists_by_user_id_and_role_id(self, user_id: int, role_id: int) -> bool:
        stmt = select(func.count(MyRolesEntity.id)).where(
            and_(
                MyRolesEntity.role_id == role_id,
                MyRolesEntity.user_id == user_id
            )
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_by_user_id_and_role_id(self, user_id: int, role_id: int) -> (MyRolesEntity | None):
        stmt = select(MyRolesEntity).where(
            and_(
                MyRolesEntity.role_id == role_id,
                MyRolesEntity.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()