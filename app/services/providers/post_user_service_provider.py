from app.services.base.post_user_service_base import PostUserServiceBase
from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from app.repositories.providers.post_user_repository_provider import PostUserRepositoryProvider
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from app.utils.filter.post_user_filter import PostUserFilter
from typing import Final

class PostUserServiceProvider(PostUserServiceBase):
    def __init__(self, repository: PostUserRepositoryProvider):
        self.repository = repository

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def get_all_filter(self, filter: PostUserFilter) -> list[PostUserEntity]:
        return await self.repository.get_all_filter(filter)

    async def create(self, user: UserEntity, category: CategoryEntity, dto: CreatePostUserDTO) -> PostUserEntity:
        post: Final = dto.to_entity()
        post.user_id = user.id
        post.category_id = category.id

        return await self.repository.create(post)

    async def update(self, post: PostUserEntity, dto: UpdatePostUserDTO) -> PostUserEntity:
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(post, field, value)

        return await self.repository.save(post)

    async def get_by_id(self, id: int) -> (PostUserEntity | None):
        if id is None or id <= 0:
            return None

        return await self.repository.get_by_id(id)

    async def delete(self, post: PostUserEntity):
        await self.repository.delete(post)