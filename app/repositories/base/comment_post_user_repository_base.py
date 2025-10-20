from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostUserEntity
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter


class CommentPostUserRepositoryBase(ABC):
    pass