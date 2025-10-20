from app.configs.db.database import PostEnterpriseEntity
from abc import ABC, abstractmethod
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter

class PostEnterpriseServiceBase(ABC):

    @abstractmethod
    async def update(self, post: PostEnterpriseEntity, dto: UpdatePostEnterpriseDTO) -> PostEnterpriseEntity:
        pass

    @abstractmethod
    async def create(self, enterprise_id: int, category_id: int, dto: CreatePostEnterpriseDTO) -> PostEnterpriseEntity:
        pass