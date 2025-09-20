from abc import ABC, abstractmethod
from app.configs.db.database import IndustryEntity
from app.schemas.industry_schemas import CreateIndustryDTO, UpdateIndustryDTO

class IndustryServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> IndustryEntity | None:
        pass

    @abstractmethod
    async def delete(self, industry: IndustryEntity):
        pass

    @abstractmethod
    async def create(self, dto: CreateIndustryDTO) -> IndustryEntity:
        pass

