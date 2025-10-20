from app.services.base.post_enterprise_service_base import PostEnterpriseServiceBase
from app.configs.db.database import PostEnterpriseEntity
from app.repositories.providers.post_enterprise_repository_provider import PostEnterpriseRepositoryProvider
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO
from app.services.generics.generic_service import GenericService
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from typing import Final
from datetime import datetime

class PostEnterpriseServiceProvider(
    PostEnterpriseServiceBase,
    GenericService[
        PostEnterpriseEntity,
        PostEnterpriseRepositoryProvider,
        PostEnterpriseFilter,
    ]
):
    def __init__(self, repository: PostEnterpriseRepositoryProvider):
        super().__init__(repository)

    async def create(self, enterprise_id: int, category_id: int, dto: CreatePostEnterpriseDTO) -> PostEnterpriseEntity:
        post: Final = dto.to_entity()
        post.enterprise_id = enterprise_id
        post.category_id = category_id

        return await self.repository.create(post)

    async def update(self, post: PostEnterpriseEntity, dto: UpdatePostEnterpriseDTO) -> PostEnterpriseEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(post, field, value)

        post.updated_at = datetime.now()
        return await self.repository.save(post)