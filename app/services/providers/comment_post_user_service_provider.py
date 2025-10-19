from abc import ABC

from app.configs.db.database import CommentPostUserEntity
from app.repositories.providers.comment_post_user_repository_provider import CommentPostUserRepositoryProvider
from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.services.base.comment_post_user_service_base import CommentPostUserServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserServiceProvider(
    CommentPostUserServiceBase,
    GenericService[
        CommentPostUserEntity,
        CommentPostUserRepositoryProvider,
        CommentPostUserFilter
    ]
):
    def __init__(self, repository: CommentPostUserRepositoryProvider):
        super().__init__(repository)

    async def create(self, user_id: int, dto: CreateCommentPostUserDTO) -> CommentPostUserEntity:
        comment = dto.to_entity()
        comment.user_id = user_id

        return await self.repository.add(comment)

    async def update(self, comment: CommentPostUserEntity, dto: UpdateCommentPostUserDTO) -> CommentPostUserEntity:
        if dto.content is not None:
            comment.content = dto.content

        comment.is_edited = True
        return await self.repository.add(comment)