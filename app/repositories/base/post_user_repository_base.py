from abc import ABC, abstractmethod
from app.configs.db.database import PostUserEntity
from app.utils.filter.post_user_filter import PostUserFilter

class PostUserRepositoryBase(ABC):
    
    @abstractmethod
    async def get_by_id(self, id: int) -> PostUserEntity | None :
        pass

    @abstractmethod
    async def delete(self, post: PostUserEntity) -> None:
        pass

    @abstractmethod
    async def create(self, post: PostUserEntity) -> PostUserEntity:
        pass

    @abstractmethod
    async def save(self, post: PostUserEntity) -> PostUserEntity:
        pass

    @abstractmethod
    async def get_all_filter(self, filter: PostUserFilter) -> list[PostUserEntity]:
        pass
    

