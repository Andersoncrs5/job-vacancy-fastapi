from app.configs.db.database import UserRolesEntity
from app.repositories.providers.my_roles_repository_provider import MyRolesRepositoryProvider
from app.services.base.my_roles_service_base import MyRolesServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.my_role_filter import MyRolesFilter


class MyRolesServiceProvider(
    MyRolesServiceBase,
    GenericService[
        UserRolesEntity,
        MyRolesRepositoryProvider,
        MyRolesFilter
    ]
):
    def __init__(self, repository: MyRolesRepositoryProvider):
        super().__init__(repository)

    async def create(self, user_id: int, role_id: int):
        my = UserRolesEntity()
        my.role_id = role_id
        my.user_id = user_id

        return await self.repository.add(my)

    async def exists_by_user_id_and_role_id(self, user_id: int, role_id: int) -> bool:
        return await self.repository.exists_by_user_id_and_role_id(
            user_id=user_id,
            role_id=role_id
        )

    async def get_by_user_id_and_role_id(self, user_id: int, role_id: int) -> UserRolesEntity | None:
        return await self.repository.get_by_user_id_and_role_id(
            user_id=user_id,
            role_id=role_id
        )