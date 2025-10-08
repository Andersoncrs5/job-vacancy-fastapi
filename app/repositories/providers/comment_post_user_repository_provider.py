from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base.comment_post_user_repository_base import CommentPostUserRepositoryBase


class CommentPostUserRepositoryProvider(CommentPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db