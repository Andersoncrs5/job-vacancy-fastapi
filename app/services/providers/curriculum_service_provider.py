from app.configs.db.database import CurriculumEntity
from app.repositories.providers.curriculum_repository_provider import CurriculumRepositoryProvider
from app.schemas.curriculum_schemas import CreateCurriculumDTO, UpdateCurriculumDTO
from app.services.base.curriculum_service_base import CurriculumServiceBase

class CurriculumServiceProvider(CurriculumServiceBase):
    def __init__(self, repository: CurriculumRepositoryProvider):
        self.repository = repository

    async def update(self, curri: CurriculumEntity, dto: UpdateCurriculumDTO) -> CurriculumEntity:
        if dto.title is not None:
            curri.title = dto.title

        if dto.is_updated is not None:
            curri.is_updated = dto.is_updated

        if dto.is_visible is not None:
            curri.is_visible = dto.is_visible

        if dto.description is not None:
            curri.description = dto.description

        return await self.repository.save(curri)

    async def create(self, user_id: int, dto: CreateCurriculumDTO) -> CurriculumEntity:
        curry = dto.to_entity()
        curry.user_id = user_id

        return await self.repository.add(curry)

    async def get_by_user_id(self, user_id: int) -> CurriculumEntity | None:
        return await self.repository.get_by_user_id(user_id)

    async def exists_by_user_id(self, user_id: int) -> bool:
        return await self.repository.exists_by_user_id(user_id)

    async def toggle_status_is_updated(self, curri: CurriculumEntity) -> CurriculumEntity:
        curri.is_updated = not curri.is_updated

        return await self.repository.save(curri)