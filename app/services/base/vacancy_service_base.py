from abc import ABC, abstractmethod
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import List
from app.schemas.vacancy_schemas import CreateVacancyDTO, UpdateVacancyDTO

class VacancyServiceBase(ABC):

    @abstractmethod
    async def update(self, vacancy: VacancyEntity, dto: UpdateVacancyDTO) -> VacancyEntity:
        pass
    
    @abstractmethod
    async def create(self, enterprise_id: int, dto: CreateVacancyDTO) -> VacancyEntity:
        pass