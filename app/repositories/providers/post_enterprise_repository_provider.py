from app.repositories.base.post_user_repository_base import *
from app.configs.db.database import PostEnterpriseEntity
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.post_enterprise_filter import PostEnterpriseFilter
from sqlalchemy import select, func, Result, Select
from typing import Final, Tuple
from app.repositories.base.post_enterprise_repository_base import PostEnterpriseRepositoryBase

class PostEnterpriseRepositoryProvider(
    PostEnterpriseRepositoryBase,
    GenericRepository[
        PostEnterpriseEntity,
        PostEnterpriseFilter,
        int,
        PostEnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=PostEnterpriseEntity)