from abc import ABC, abstractmethod
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import List
from app.schemas.vacancy_schemas import CreateVacancyDTO, UpdateVacancyDTO

class VacancyServiceBase(ABC):

    @abstractmethod
    async def delete(self, vacancy: VacancyEntity):
        pass
    
    @abstractmethod
    async def get_all(self, filter: VacancyFilter) -> List[VacancyEntity]:
        pass

    @abstractmethod
    async def update(self, vacancy: VacancyEntity, dto: UpdateVacancyDTO) -> VacancyEntity:
        pass
    
    @abstractmethod
    async def create(self, enterprise_id: int, dto: CreateVacancyDTO) -> VacancyEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> VacancyEntity | None:
        pass

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass