from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.configs.db.database import CommentPostUserEntity
from app.repositories.base.comment_post_user_repository_base import CommentPostUserRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserRepositoryProvider(
    CommentPostUserRepositoryBase,
    GenericRepository[
        CommentPostUserEntity,
        CommentPostUserFilter,
        int,
        CommentPostUserEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=CommentPostUserEntity)