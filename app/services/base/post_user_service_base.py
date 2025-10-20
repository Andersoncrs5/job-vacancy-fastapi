from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from abc import ABC, abstractmethod
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from app.utils.filter.post_user_filter import PostUserFilter

class PostUserServiceBase(ABC):

    @abstractmethod
    async def update(self, post: PostUserEntity, dto: UpdatePostUserDTO) -> PostUserEntity:
        pass

    @abstractmethod
    async def create(self, user: UserEntity, category: CategoryEntity, dto: CreatePostUserDTO) -> PostUserEntity:
        pass