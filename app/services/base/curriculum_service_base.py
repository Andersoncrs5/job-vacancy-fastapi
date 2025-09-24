from abc import ABC, abstractmethod
from app.configs.db.database import CurriculumEntity
from app.schemas.curriculum_schemas import CreateCurriculumDTO, UpdateCurriculumDTO

class CurriculumServiceBase(ABC):

    @abstractmethod
    async def toggle_status_is_updated(self, curri: CurriculumEntity) -> CurriculumEntity:
        pass

    @abstractmethod
    async def update(self, curri: CurriculumEntity, dto: UpdateCurriculumDTO) -> CurriculumEntity:
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def create(self, user_id: int, dto: CreateCurriculumDTO) -> CurriculumEntity:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> CurriculumEntity | None:
        pass
