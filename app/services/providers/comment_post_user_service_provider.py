from abc import ABC

from app.configs.db.database import CommentPostUserEntity
from app.repositories.providers.comment_post_user_repository_provider import CommentPostUserRepositoryProvider
from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.services.base.comment_post_user_service_base import CommentPostUserServiceBase
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserServiceProvider(CommentPostUserServiceBase, ABC):
    def __init__(self, repository: CommentPostUserRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, id: int) -> CommentPostUserEntity | None:
        return await self.repository.get_by_id(id)

    async def delete(self, comment: CommentPostUserEntity):
        await self.repository.delete(comment)

    async def get_all(self, filter: CommentPostUserFilter) -> list[CommentPostUserEntity]:
        return await self.repository.get_all(filter)

    async def exists_by_id(self, id: int) -> bool:
        return await self.repository.exists_by_id(id)

    async def create(self, user_id: int, dto: CreateCommentPostUserDTO) -> CommentPostUserEntity:
        comment = dto.to_entity()
        comment.user_id = user_id

        return await self.repository.add(comment)

    async def update(self, comment: CommentPostUserEntity, dto: UpdateCommentPostUserDTO) -> CommentPostUserEntity:
        if dto.content is not None:
            comment.content = dto.content

        return await self.repository.add(comment)