from abc import ABC, abstractmethod
from app.configs.db.database import VacancySkillEntity
from app.schemas.vacancy_skill_schemas import VacancySkillOUT
from app.utils.filter.vacancy_skill_filter import VacancySkillFilter


class VacancySkillRepositoryBase(ABC):

    @abstractmethod
    async def get_all_by_vacancy_id(self, vacancy_id: int) -> list[VacancySkillEntity]:
        pass

    @abstractmethod
    async def exists_by_vacancy_id_and_skill_id(self,vacancy_id: int, skill_id: int) -> bool:
        pass
