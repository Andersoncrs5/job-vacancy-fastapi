from typing import List
from app.configs.db.database import MediaPostUserEntity
from app.repositories.providers.media_post_user_repository_provider import MediaPostUserRepositoryProvider
from app.schemas.media_post_user_schemas import CreateMediaPostUserDTO, UpdateMediaPostUserDTO
from app.services.base.media_post_user_service_base import MediaPostUserServiceBase
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter


class MediaPostUserServiceProvider(MediaPostUserServiceBase):
    def __init__(self, repository: MediaPostUserRepositoryProvider):
        self.repository = repository

    async def update(self, media: MediaPostUserEntity, dto: UpdateMediaPostUserDTO) -> MediaPostUserEntity:
        if dto.url != None:
            media.url = dto.url

        if dto.type != None:
            media.type = dto.type

        if dto.order != None:
            media.order = dto.order

        if dto.caption != None:
            media.caption = dto.caption

        if dto.size != None:
            media.size = dto.size

        if dto.mime_type != None:
            media.mime_type = dto.mime_type
        
        return await self.repository.save(media)

    async def get_amount_by_post_id(self, post_id: int) -> int:
        return await self.repository.get_amount_by_post_id(post_id)

    async def create(self, post_id: int, dto: CreateMediaPostUserDTO) -> MediaPostUserEntity:
        media_entity = dto.to_entity()
        media_entity.post_id = post_id

        return await self.repository.add(media_entity)

    async def get_all_filter(self, filter: MediaPostUserFilter) -> List[MediaPostUserFilter]:
        return await self.repository.get_all_filter(filter)

    async def delete(self, media: MediaPostUserEntity):
        await self.repository.delete(media)

    async def get_by_id(self, id: int) -> MediaPostUserEntity | None:
        if id <= 0:
            return None

        return await self.repository.get_by_id(id)