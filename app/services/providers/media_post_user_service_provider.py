from typing import List
from app.configs.db.database import MediaPostUserEntity
from app.repositories.providers.media_post_user_repository_provider import MediaPostUserRepositoryProvider
from app.schemas.media_post_user_schemas import CreateMediaPostUserDTO, UpdateMediaPostUserDTO
from app.services.base.media_post_user_service_base import MediaPostUserServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter


class MediaPostUserServiceProvider(
    MediaPostUserServiceBase,
    GenericService[
        MediaPostUserEntity,
        MediaPostUserRepositoryProvider,
        MediaPostUserFilter
    ]
):
    def __init__(self, repository: MediaPostUserRepositoryProvider):
        super().__init__(repository)

    async def update(self, media: MediaPostUserEntity, dto: UpdateMediaPostUserDTO) -> MediaPostUserEntity:
        updates = dto.model_dump(exclude_none=True)

        for field, value in updates.items():
            setattr(media, field, value)
        
        return await self.repository.save(media)

    async def get_amount_by_post_id(self, post_id: int) -> int:
        return await self.repository.get_amount_by_post_id(post_id)

    async def create(self, post_id: int, dto: CreateMediaPostUserDTO) -> MediaPostUserEntity:
        media_entity = dto.to_entity()
        media_entity.post_id = post_id

        return await self.repository.add(media_entity)