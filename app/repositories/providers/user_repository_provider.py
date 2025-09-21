from app.repositories.base.user_repository_base import UserRepositoryBase
from app.configs.db.database import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Final

class UserRepositoryProvider(UserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_by_id(self, id: int) -> bool:
        stmt = select(func.count(UserEntity.id)).where(UserEntity.id == id)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def get_by_id(self, id: int) -> (UserEntity | None):
        stmt: Final = select(UserEntity).where(UserEntity.id == id)
        
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_email(self, email: str) -> (UserEntity | None):
        stmt: Final = select(UserEntity).where(UserEntity.email == email)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, user: UserEntity):
        await self.db.delete(user)
        await self.db.commit()

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(func.count(UserEntity.id)).where(UserEntity.email == email)

        result: Final[int | None] = await self.db.scalar(stmt)

        if result is None:
            return False

        return result > 0

    async def add(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def save(self, user: UserEntity) -> UserEntity:
        await self.db.commit()
        await self.db.refresh(user)

        return user