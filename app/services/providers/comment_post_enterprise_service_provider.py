from app.configs.db.database import CommentPostEnterpriseEntity
from app.repositories.providers.comment_post_enterprise_repository_provider import \
    CommentPostEnterpriseRepositoryProvider
from app.schemas.comment_post_enterprise_schemas import CreateCommentPostEnterpriseDTO, UpdateCommentPostEnterpriseDTO
from app.services.base.comment_post_enterprise_service_base import CommentPostEnterpriseServiceBase
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseServiceProvider(CommentPostEnterpriseServiceBase):
    def __init__(self, repository: CommentPostEnterpriseRepositoryProvider):
        self.repository = repository

    async def update(self, comment: CommentPostEnterpriseEntity, dto: UpdateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        if dto.content is not None:
            comment.content = dto.content

        comment.is_edited = True
        return await self.repository.add(comment)

    async def create(self, user_id: int, dto: CreateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        comment = dto.to_entity()
        comment.user_id = user_id

        return await self.repository.add(comment)

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def get_by_id(self, id: int) -> CommentPostEnterpriseEntity | None:
        return await self.repository.get_by_id(id)

    async def delete(self, comment: CommentPostEnterpriseEntity):
        await self.repository.delete(comment)

    async def get_all(self, filter: CommentPostEnterpriseFilter) -> list[CommentPostEnterpriseEntity]:
        return await self.repository.get_all(filter)