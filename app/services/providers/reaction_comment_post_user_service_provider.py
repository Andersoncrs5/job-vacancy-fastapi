from app.repositories.providers.reaction_comment_post_user_repository_provider import \
    ReactionCommentPostUserRepositoryProvider
from app.services.base.reaction_comment_post_user_service_base import ReactionCommentPostUserServiceBase


class ReactionCommentPostUserServiceProvider(ReactionCommentPostUserServiceBase):
    def __init__(self, repository: ReactionCommentPostUserRepositoryProvider):
        self.repository = repository