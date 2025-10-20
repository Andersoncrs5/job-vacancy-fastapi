from app.repositories.base.saved_search_repository_base import SavedSearchReposioryBase
from app.configs.db.database import SavedSearchEntity
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.saved_search_filter import SavedSearchFilter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, func
from typing import List, Final

class SavedSearchReposioryProvider(
    SavedSearchReposioryBase,
    GenericRepository[
        SavedSearchEntity,
        SavedSearchFilter,
        int,
        SavedSearchEntity,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=SavedSearchEntity)