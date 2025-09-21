from app.services.base.user_service_base import UserServiceBase
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.configs.db.database import UserEntity
from app.schemas.user_schemas import CreateUserDTO, UpdateUserDTO
from app.services.providers.crypto_service import hash_password
from typing import Final

class UserServiceProvider(UserServiceBase):
    def __init__(self, repository: UserRepositoryProvider):
        self.repository = repository

    async def create(self, dto: CreateUserDTO) -> UserEntity: 
        user_mapped: Final[UserEntity] = dto.to_user_entity()

        user_mapped.password = hash_password(user_mapped.password)

        return await self.repository.add(user_mapped)

    async def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        if dto.name != None :
            user.name = dto.name

        if dto.avatar_url != None :
            user.avatar_url = dto.avatar_url

        if dto.bio != None :
            user.bio = dto.bio

        if dto.password != None :
            user.password = hash_password(dto.password)

        return await self.repository.save(user)

    async def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        user.refresh_token = refresh_token

        return await self.repository.save(user)

    async def exists_by_email(self, email: str) -> bool:
        return await self.repository.exists_by_email(email)

    async def get_by_id(self, id: int) -> (UserEntity | None):
        if id <= 0 or id is None:
            return None

        return await self.repository.get_by_id(id)

    async def get_by_email(self, email: str) -> (UserEntity | None):
        if not email or not email.strip() or email is None:
            return None

        return await self.repository.get_by_email(email)

    async def delete(self, user: UserEntity):
        await self.repository.delete(user)