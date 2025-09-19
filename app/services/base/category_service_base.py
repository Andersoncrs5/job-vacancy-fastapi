from abc import ABC, abstractmethod
from app.configs.db.database import CategoryEntity, UserEntity
from app.schemas.category_schemas import CreateCategoryDTO, UpdateCategoryDTO
from app.utils.filter.category_filter import CategoryFilter
from app.utils.enums.sum_red import SumRedEnum

class CategoryServiceBase(ABC):

    @abstractmethod
    async def get_all(self, is_active: bool) -> list[CategoryEntity]:
        pass

    @abstractmethod
    async def get_all_filter(self, is_active: bool, filter: CategoryFilter) -> list[CategoryEntity]:
        pass

    @abstractmethod
    async def create(self, user: UserEntity, dto: CreateCategoryDTO) -> CategoryEntity:
        pass

    @abstractmethod
    async def toggle_is_active(self, category: CategoryEntity) -> CategoryEntity:
        pass

    @abstractmethod
    async def update(self, category: CategoryEntity, dto: UpdateCategoryDTO) -> CategoryEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> CategoryEntity | None:
        pass

    @abstractmethod
    async def delete(self, category: CategoryEntity):
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    async def sum_red_job_count(self, category: CategoryEntity, action: SumRedEnum) -> CategoryEntity:
        pass
    
    @abstractmethod
    async def sum_red_post_count(self, category: CategoryEntity, action: SumRedEnum) -> CategoryEntity:
        pass

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool :
        pass