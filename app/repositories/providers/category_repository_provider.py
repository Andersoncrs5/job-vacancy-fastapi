from app.repositories.base.category_repository_base import CategoryRepositoryBase
from app.configs.db.database import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Final

class CategoryRepositoryProvider(CategoryRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db