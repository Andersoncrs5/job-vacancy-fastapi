from app.services.base.vacancy_skill_service_base import VacancySkillServiceBase
from app.configs.db.database import VacancySkillEntity
from app.schemas.vacancy_skill_schemas import CreateVacancySkillDTO, UpdateVacancySkillDTO
from app.repositories.providers.vacancy_skill_repository_provider import VacancySkillRepositoryProvider
from app.services.generics.generic_service import GenericService
from app.utils.filter.vacancy_skill_filter import VacancySkillFilter


class VacancySkillServiceProvider(
    VacancySkillServiceBase,
    GenericService[
        VacancySkillEntity,
        VacancySkillRepositoryProvider,
        VacancySkillFilter
    ]
):
    def __init__(self, repository: VacancySkillRepositoryProvider):
        super().__init__(repository)

    async def update(self, vs: VacancySkillEntity, dto: UpdateVacancySkillDTO) -> VacancySkillEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(vs, field, value)

        return await self.repository.save(vs)

    async def get_all_by_vacancy_id(self, vacancy_id: int) -> list[VacancySkillEntity]:
        return await self.repository.get_all_by_vacancy_id(vacancy_id)

    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        return await self.repository.exists_by_vacancy_id_and_skill_id(vacancy_id, skill_id)

    async def create(self, dto: CreateVacancySkillDTO) -> VacancySkillEntity:
        vs = dto.to_entity()

        return await self.repository.add(vs)

    async def toggle_is_required(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        vs.is_required = not vs.is_required
        return await self.repository.save(vs)
