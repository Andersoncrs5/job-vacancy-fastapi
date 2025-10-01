from abc import ABC, abstractmethod
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import List

class VacancyRepositoryBase(ABC):
    
    @abstractmethod
    async def get_all(self, filter: VacancyFilter) -> List[VacancyEntity]:
        pass

    @abstractmethod
    async def add(self, vacancy: VacancyEntity) -> VacancyEntity:
        pass
    
    @abstractmethod
    async def save(self, vacancy: VacancyEntity) -> VacancyEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> VacancyEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass