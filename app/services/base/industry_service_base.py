from abc import ABC, abstractmethod
from app.configs.db.database import IndustryEntity, UserEntity
from app.schemas.industry_schemas import CreateIndustryDTO, UpdateIndustryDTO
from app.utils.filter.industry_filter import IndustryFilter

class IndustryServiceBase(ABC):

    @abstractmethod
    async def get_all_filter(self, filter: IndustryFilter) -> list[IndustryEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> IndustryEntity | None:
        pass

    @abstractmethod
    async def delete(self, industry: IndustryEntity):
        pass

    @abstractmethod
    async def create(self, user: UserEntity, dto: CreateIndustryDTO) -> IndustryEntity:
        pass

    @abstractmethod
    async def update(self, industry: IndustryEntity, dto: UpdateIndustryDTO) -> IndustryEntity:
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def toggle_is_active(self, industry: IndustryEntity) -> IndustryEntity:
        pass


    