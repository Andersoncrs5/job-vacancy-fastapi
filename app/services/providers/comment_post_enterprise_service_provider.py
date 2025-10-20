from app.configs.db.database import CommentPostEnterpriseEntity
from app.repositories.providers.comment_post_enterprise_repository_provider import \
    CommentPostEnterpriseRepositoryProvider
from app.schemas.comment_post_enterprise_schemas import CreateCommentPostEnterpriseDTO, UpdateCommentPostEnterpriseDTO
from app.services.base.comment_post_enterprise_service_base import CommentPostEnterpriseServiceBase
from app.services.generics.generic_service import GenericService
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseServiceProvider(
    CommentPostEnterpriseServiceBase,
    GenericService[
        CommentPostEnterpriseEntity,
        CommentPostEnterpriseRepositoryProvider,
        CommentPostEnterpriseFilter
    ]
):
    def __init__(self, repository: CommentPostEnterpriseRepositoryProvider):
        super().__init__(repository)

    async def update(self, comment: CommentPostEnterpriseEntity, dto: UpdateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        if dto.content is not None:
            comment.content = dto.content

        comment.is_edited = True
        return await self.repository.add(comment)

    async def create(self, user_id: int, dto: CreateCommentPostEnterpriseDTO) -> CommentPostEnterpriseEntity:
        comment = dto.to_entity()
        comment.user_id = user_id

        return await self.repository.add(comment)