from abc import ABC, abstractmethod
from app.configs.db.database import PostEnterpriseEntity
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter

class PostEnterpriseRepositoryBase(ABC):
    
    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> PostEnterpriseEntity | None :
        pass

    @abstractmethod
    async def delete(self, post: PostEnterpriseEntity) -> None:
        pass

    @abstractmethod
    async def create(self, post: PostEnterpriseEntity) -> PostEnterpriseEntity:
        pass

    @abstractmethod
    async def save(self, post: PostEnterpriseEntity) -> PostEnterpriseEntity:
        pass

    @abstractmethod
    async def get_all(self, filter: PostEnterpriseFilter) -> list[PostEnterpriseEntity]:
        pass
    

