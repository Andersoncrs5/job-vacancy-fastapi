from app.configs.db.database import ApplicationEntity
from app.repositories.providers.application_repository_provider import ApplicationRepositoryProvider
from app.schemas.application_schemas import UpdateApplicationDTO
from app.services.base.application_service_base import ApplicationServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.applications_filter import ApplicationFilter

class ApplicationServiceProvider(
    ApplicationServiceBase,
    GenericService[
        ApplicationEntity,
        ApplicationRepositoryProvider,
        ApplicationFilter
    ]
):
    def __init__(self, repository: ApplicationRepositoryProvider):
        super().__init__(repository)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def update(self, app: ApplicationEntity, dto: UpdateApplicationDTO) -> ApplicationEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(app, field, value)

        return await self.repository.save(app)

    async def exists_by_application(self, user_id: int, vacancy_id: int) -> bool:
        return await self.repository.exists_by_application(user_id, vacancy_id)

    async def create(self, vacancy_id: int, user_id: int) -> ApplicationEntity:
        app = ApplicationEntity(vacancy_id=vacancy_id, user_id=user_id)

        return await self.repository.add(app)