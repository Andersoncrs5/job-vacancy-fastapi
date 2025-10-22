from app.configs.db.database import RolesEntity
from app.repositories.providers.roles_repository_provider import RolesRepositoryProvider
from app.services.base.roles_service_base import RolesServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.roles_filter import RolesFilter


class RolesServiceProvider(
    RolesServiceBase,
    GenericService[
        RolesEntity,
        RolesRepositoryProvider,
        RolesFilter
    ]
):
    def __init__(self, repository: RolesRepositoryProvider):
        super().__init__(repository)

    async def get_by_title(self, title: str) -> RolesEntity | None:
        return await self.repository.get_by_title(title=title)