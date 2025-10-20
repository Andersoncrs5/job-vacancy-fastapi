from app.services.base.post_user_service_base import PostUserServiceBase
from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from app.repositories.providers.post_user_repository_provider import PostUserRepositoryProvider
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO
from app.services.generics.generic_service import GenericService
from app.utils.filter.post_user_filter import PostUserFilter
from typing import Final
from datetime import datetime

class PostUserServiceProvider(
    PostUserServiceBase,
    GenericService[
        PostUserEntity,
        PostUserRepositoryProvider,
        PostUserFilter,
    ]
):
    def __init__(self, repository: PostUserRepositoryProvider):
        super().__init__(repository)

    async def create(self, user: UserEntity, category: CategoryEntity, dto: CreatePostUserDTO) -> PostUserEntity:
        post: Final = dto.to_entity()
        post.user_id = user.id
        post.category_id = category.id

        return await self.repository.create(post)

    async def update(self, post: PostUserEntity, dto: UpdatePostUserDTO) -> PostUserEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(post, field, value)

        post.updated_at = datetime.now()
        return await self.repository.save(post)