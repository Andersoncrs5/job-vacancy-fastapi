from app.configs.db.database import PostEnterpriseEntity
from abc import ABC, abstractmethod
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter

class PostEnterpriseServiceBase(ABC):

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, filter: PostEnterpriseFilter) -> list[PostEnterpriseEntity]:
        pass

    @abstractmethod
    async def update(self, post: PostEnterpriseEntity, dto: UpdatePostEnterpriseDTO) -> PostEnterpriseEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> PostEnterpriseEntity | None:
        pass

    @abstractmethod
    async def delete(self, post: PostEnterpriseEntity) -> None:
        pass

    @abstractmethod
    async def create(self, enterprise_id: int, category_id: int, dto: CreatePostEnterpriseDTO) -> PostEnterpriseEntity:
        pass