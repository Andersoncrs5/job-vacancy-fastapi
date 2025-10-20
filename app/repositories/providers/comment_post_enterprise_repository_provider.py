from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import CommentPostEnterpriseEntity
from app.repositories.base.comment_post_enterprise_repository_base import CommentPostEnterpriseRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseRepositoryProvider(
    CommentPostEnterpriseRepositoryBase,
    GenericRepository[
        CommentPostEnterpriseEntity,
        CommentPostEnterpriseFilter,
        int,
        CommentPostEnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=CommentPostEnterpriseEntity)