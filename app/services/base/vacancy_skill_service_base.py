from abc import ABC, abstractmethod

from app.configs.db.database import VacancySkillEntity
from app.schemas.vacancy_skill_schemas import CreateVacancySkillDTO, UpdateVacancySkillDTO

class VacancySkillServiceBase(ABC):

    @abstractmethod
    async def toggle_is_required(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> VacancySkillEntity | None:
        pass

    @abstractmethod
    async def delete(self, vs: VacancySkillEntity):
        pass

    @abstractmethod
    async def create(self, dto: CreateVacancySkillDTO) -> VacancySkillEntity:
        pass

    @abstractmethod
    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        pass

    @abstractmethod
    async def update(self, vs: VacancySkillEntity, dto: UpdateVacancySkillDTO) -> VacancySkillEntity:
        pass

    @abstractmethod
    async def get_all(self, vacancy_id: int) -> list[VacancySkillEntity]:
        pass