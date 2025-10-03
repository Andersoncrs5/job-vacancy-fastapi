from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import AddressUserEntity
from app.repositories.base.address_user_repository_base import AddressUserRepositoryBase
from sqlalchemy import select, func, Result
from datetime import datetime

class AddressUserRepositoryProvider(AddressUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, address: AddressUserEntity) -> AddressUserEntity:
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)

        return address

    async def save(self, address: AddressUserEntity) -> AddressUserEntity:
        address.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(address)

        return address

    async def delete(self, address: AddressUserEntity):
        await self.db.delete(address)
        await self.db.commit()

    async def exists_by_user_id(self, user_id: int) -> bool:
        stmt = select(func.count(AddressUserEntity.id)).where(
            AddressUserEntity.user_id == user_id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)
        
    async def get_by_id(self, id: int) -> AddressUserEntity | None:
        result = await self.db.execute(
            select(AddressUserEntity).where(AddressUserEntity.id == id)
        )

        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> AddressUserEntity | None:
        result = await self.db.execute(
            select(AddressUserEntity).where(AddressUserEntity.user_id == user_id)
        )

        return result.scalars().first()