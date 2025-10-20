from app.services.base.user_service_base import UserServiceBase
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.configs.db.database import UserEntity
from app.schemas.user_schemas import CreateUserDTO, UpdateUserDTO
from app.services.generics.generic_service import GenericService
from app.services.providers.crypto_service import hash_password
from typing import Final
from app.utils.filter.user_filter import UserFilter

class UserServiceProvider(
    UserServiceBase,
    GenericService[
        UserEntity,
        UserRepositoryProvider,
        UserFilter,
    ]
):
    def __init__(self, repository: UserRepositoryProvider):
        super().__init__(repository)

    async def create(self, dto: CreateUserDTO) -> UserEntity: 
        user_mapped: Final[UserEntity] = dto.to_user_entity()

        user_mapped.password = hash_password(user_mapped.password)

        return await self.repository.add(user_mapped)

    async def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        if dto.name is not None:
            user.name = dto.name

        if dto.avatar_url is not None:
            user.avatar_url = dto.avatar_url

        if dto.bio is not None:
            user.bio = dto.bio

        if dto.password is not None:
            user.password = hash_password(dto.password)

        return await self.repository.save(user)

    async def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        user.refresh_token = refresh_token

        return await self.repository.save(user)

    async def exists_by_email(self, email: str) -> bool:
        return await self.repository.exists_by_email(email)

    async def get_by_email(self, email: str) -> (UserEntity | None):
        if not email or not email.strip() or email is None:
            return None

        return await self.repository.get_by_email(email)