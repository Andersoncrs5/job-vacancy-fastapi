from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from abc import ABC, abstractmethod
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, UpdateSavedSearchOUT
from app.utils.filter.saved_search_filter import SavedSearchFilter

class SavedSearchServiceBase(ABC):
    