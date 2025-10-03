from app.configs.db.database import AddressUserEntity
from app.services.base.address_user_service_base import AddressUserServiceBase
from app.schemas.address_user_schemas import CreateAddressUserDTO, UpdateAddressUserDTO
from app.repositories.providers.address_user_repository_provider import AddressUserRepositoryProvider

class AddressUserServiceProvider(AddressUserServiceBase):
    def __init__(self, repository: AddressUserRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, id: int) -> AddressUserEntity | None:
        return await self.repository.get_by_id(id)

    async def get_by_user_id(self, user_id: int) -> AddressUserEntity | None:
        return await self.repository.get_by_user_id(user_id)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def delete(self, address: AddressUserEntity):
        await self.repository.delete(address)

    async def create(self, user_id: int, dto: CreateAddressUserDTO) -> AddressUserEntity:
        address = dto.to_entity()
        address.user_id = user_id

        return await self.repository.add(address)

    async def update(self, address: AddressUserEntity, dto: UpdateAddressUserDTO) -> AddressUserEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(address, field, value)

        return await self.repository.save(address)