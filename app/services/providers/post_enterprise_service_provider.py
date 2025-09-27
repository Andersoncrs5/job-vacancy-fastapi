from app.services.base.post_enterprise_service_base import PostEnterpriseServiceBase
from app.configs.db.database import PostEnterpriseEntity
from app.repositories.providers.post_enterprise_repository_provider import PostEnterpriseRepositoryProvider
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from typing import Final
from datetime import datetime

class PostEnterpriseServiceProvider(PostEnterpriseServiceBase):
    def __init__(self, repository: PostEnterpriseRepositoryProvider):
        self.repository = repository

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def get_all(self, filter: PostEnterpriseFilter) -> list[PostEnterpriseEntity]:
        return await self.repository.get_all(filter)

    async def create(self, enterprise_id: int, category_id: int, dto: CreatePostEnterpriseDTO) -> PostEnterpriseEntity:
        post: Final = dto.to_entity()
        post.enterprise_id = enterprise_id
        post.category_id = category_id

        return await self.repository.create(post)

    async def update(self, post: PostEnterpriseEntity, dto: UpdatePostEnterpriseDTO) -> PostEnterpriseEntity:
        if dto.title is not None:
            post.title = dto.title

        if dto.content is not None:
            post.content = dto.content

        if dto.url_image is not None:
            post.url_image = dto.url_image

        post.updated_at = datetime.now()
        return await self.repository.save(post)

    async def get_by_id(self, id: int) -> (PostEnterpriseEntity | None):
        return await self.repository.get_by_id(id)

    async def delete(self, post: PostEnterpriseEntity):
        await self.repository.delete(post)