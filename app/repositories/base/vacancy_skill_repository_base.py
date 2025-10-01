from abc import ABC, abstractmethod
from app.configs.db.database import VacancySkillEntity
from app.schemas.vacancy_skill_schemas import VacancySkillOUT

class VacancySkillRepositoryBase(ABC):

    @abstractmethod
    async def get_all(session, vacancy_id: int) -> list[VacancySkillOUT]:
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
