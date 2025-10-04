from app.configs.db.database import AddressEnterpriseEntity
from app.services.base.address_enterprise_service_base import AddressEnterpriseServiceBase
from app.schemas.address_enterprise_schemas import CreateAddressEnterpriseDTO, UpdateAddressEnterpriseDTO
from app.repositories.providers.address_enterprise_repository_provider import AddressEnterpriseRepositoryProvider

class AddressEnterpriseServiceProvider(AddressEnterpriseServiceBase):
    def __init__(self, repository: AddressEnterpriseRepositoryProvider):
        self.repository = repository

    async def toggle_is_public(self, address: AddressEnterpriseEntity) -> AddressEnterpriseEntity:
        address.is_public = not address.is_public
        return await self.repository.save(address)

    async def get_by_enterprise_id(self, enterprise_id: int) -> AddressEnterpriseEntity | None:
        return await self.repository.get_by_enterprise_id(enterprise_id)

    async def exists_by_enterprise_id(self, enterprise_id: int) -> bool:
        return await self.repository.exists_by_enterprise_id(enterprise_id)

    async def delete(self, address: AddressEnterpriseEntity):
        await self.repository.delete(address)

    async def create(self, enterprise_id: int, dto: CreateAddressEnterpriseDTO) -> AddressEnterpriseEntity:
        address = dto.to_entity()
        address.enterprise_id = enterprise_id

        return await self.repository.add(address)

    async def update(self, address: AddressEnterpriseEntity, dto: UpdateAddressEnterpriseDTO) -> AddressEnterpriseEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(address, field, value)

        return await self.repository.save(address)