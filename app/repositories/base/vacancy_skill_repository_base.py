from abc import ABC, abstractmethod
from app.configs.db.database import VacancySkillEntity
from app.schemas.vacancy_skill_schemas import VacancySkillOUT
from app.utils.filter.vacancy_skill_filter import VacancySkillFilter


class VacancySkillRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self, filter: VacancySkillFilter) -> list[VacancySkillEntity]:
        pass

    @abstractmethod
    async def get_all_by_vacancy_id(self, vacancy_id: int) -> list[VacancySkillEntity]:
        pass

    @abstractmethod
    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> VacancySkillEntity | None:
        pass

    @abstractmethod
    async def delete(self, vs: VacancySkillEntity) -> None:
        pass

    @abstractmethod
    async def save(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        pass

    @abstractmethod
    async def add(self, vs: VacancySkillEntity) -> VacancySkillEntity:
        pass
