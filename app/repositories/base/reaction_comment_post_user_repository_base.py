from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.providers.reaction_comment_post_user_repository_provider import \
    ReactionCommentPostUserRepositoryBase


class ReactionCommentPostUserRepositoryProvider(ReactionCommentPostUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db