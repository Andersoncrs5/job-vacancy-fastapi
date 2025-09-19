from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from abc import ABC, abstractmethod
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from app.utils.filter.post_user_filter import PostUserFilter

class PostUserServiceBase(ABC):

    @abstractmethod
    async def get_all_filter(self, filter: PostUserFilter) -> list[PostUserEntity]:
        pass

    @abstractmethod
    async def update(self, post: PostUserEntity, dto: UpdatePostUserDTO) -> PostUserEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> PostUserEntity | None:
        pass

    @abstractmethod
    async def delete(self, post: PostUserEntity) -> None:
        pass

    @abstractmethod
    async def create(self, user: UserEntity, category: CategoryEntity, dto: CreatePostUserDTO) -> PostUserEntity:
        pass