from app.repositories.base.post_user_repository_base import *
from app.configs.db.database import PostUserEntity
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.post_user_filter import PostUserFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple

class PostUserRepositoryProvider(
    PostUserRepositoryBase,
    GenericRepository[
        PostUserEntity,
        PostUserFilter,
        int,
        PostUserEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=PostUserEntity)