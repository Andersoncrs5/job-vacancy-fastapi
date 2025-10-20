from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseEntity
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter


class CommentPostEnterpriseRepositoryBase(ABC):
    pass