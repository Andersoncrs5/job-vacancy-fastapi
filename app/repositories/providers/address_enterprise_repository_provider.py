from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.db.database import AddressEnterpriseEntity
from app.repositories.base.address_enterprise_repository_base import AddressEnterpriseRepositoryBase
from sqlalchemy import select, func, Result
from datetime import datetime

class AddressEnterpriseRepositoryProvider(AddressEnterpriseRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)

        return address

    async def save(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        address.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(address)

        return address

    async def delete(self, address: AddressEnterpriseEntity):
        await self.db.delete(address)
        await self.db.commit()

    async def exists_by_enterprise_id(self, enterprise_id: int) -> bool:
        stmt = select(func.count(AddressEnterpriseEntity.enterprise_id)).where(
            AddressEnterpriseEntity.enterprise_id == enterprise_id
        )

        result = await self.db.scalar(stmt)

        return bool(result and result > 0)
        
    async def get_by_enterprise_id(self, enterprise_id: int) -> AddressEnterpriseEntity | None:
        result = await self.db.execute(
            select(AddressEnterpriseEntity).where(AddressEnterpriseEntity.enterprise_id == enterprise_id)
        )

        return result.scalars().first()